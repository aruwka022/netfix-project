from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404

from .models import Service, ServiceRequest, SERVICE_FIELD_CHOICES
from .forms import CreateNewService, RequestServiceForm, RateServiceRequestForm

SERVICES_PER_PAGE = 9


def _field_choices_for(company):
    if company.field == 'All in One':
        return SERVICE_FIELD_CHOICES
    return ((company.field, company.field),)


def _search_and_sort(queryset, request):
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(name__icontains=q)

    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        queryset = queryset.order_by('price_hour')
    elif sort == 'price_desc':
        queryset = queryset.order_by('-price_hour')
    else:
        sort = 'newest'
        queryset = queryset.order_by('-date')

    return queryset, q, sort


def _extra_querystring(request):
    params = request.GET.copy()
    params.pop('page', None)
    return params.urlencode()


def _recompute_ratings(service):
    avg = service.requests.exclude(
        rating__isnull=True).aggregate(Avg('rating'))['rating__avg']
    service.rating = round(avg) if avg is not None else 0
    service.save(update_fields=['rating'])

    company = service.company
    company_avg = ServiceRequest.objects.filter(service__company=company).exclude(
        rating__isnull=True).aggregate(Avg('rating'))['rating__avg']
    company.rating = round(company_avg) if company_avg is not None else 0
    company.save(update_fields=['rating'])


def service_list(request):
    services, q, sort = _search_and_sort(Service.objects.all(), request)
    paginator = Paginator(services, SERVICES_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'services/list.html', {
        'page_obj': page_obj, 'q': q, 'sort': sort,
        'extra_qs': _extra_querystring(request),
    })


def index(request, id):
    service = get_object_or_404(Service, id=id)
    is_owner = (
        request.user.is_authenticated
        and request.user.is_company
        and service.company.user_id == request.user.id
    )
    return render(request, 'services/single_service.html', {
        'service': service, 'is_owner': is_owner,
    })


@login_required
def create(request):
    if not request.user.is_company:
        return redirect('services_list')

    company = request.user.company
    choices = _field_choices_for(company)

    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=choices)
        if form.is_valid():
            Service.objects.create(
                company=company,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_hour=form.cleaned_data['price_hour'],
                field=form.cleaned_data['field'],
            )
            return redirect('company_profile', name=request.user.username)
    else:
        form = CreateNewService(choices=choices)

    return render(request, 'services/create.html', {'form': form})


@login_required
def edit_service(request, id):
    service = get_object_or_404(Service, id=id)

    if not request.user.is_company or service.company.user_id != request.user.id:
        return redirect('index', id=id)

    choices = _field_choices_for(service.company)

    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=choices)
        if form.is_valid():
            service.name = form.cleaned_data['name']
            service.description = form.cleaned_data['description']
            service.price_hour = form.cleaned_data['price_hour']
            service.field = form.cleaned_data['field']
            service.save()
            return redirect('index', id=service.id)
    else:
        form = CreateNewService(choices=choices, initial={
            'name': service.name,
            'description': service.description,
            'price_hour': service.price_hour,
            'field': service.field,
        })

    return render(request, 'services/edit.html', {'form': form, 'service': service})


@login_required
def delete_service(request, id):
    service = get_object_or_404(Service, id=id)

    if not request.user.is_company or service.company.user_id != request.user.id:
        return redirect('index', id=id)

    if request.method == 'POST':
        username = request.user.username
        service.delete()
        return redirect('company_profile', name=username)

    return render(request, 'services/delete_confirm.html', {'service': service})


def service_field(request, field):
    field = field.replace('-', ' ').title()
    services, q, sort = _search_and_sort(
        Service.objects.filter(field=field), request)
    paginator = Paginator(services, SERVICES_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'services/field.html', {
        'page_obj': page_obj, 'field': field, 'q': q, 'sort': sort,
        'extra_qs': _extra_querystring(request),
    })


@login_required
def request_service(request, id):
    service = get_object_or_404(Service, id=id)

    if not request.user.is_customer:
        return redirect('index', id=id)

    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            service_time = form.cleaned_data['service_time']
            ServiceRequest.objects.create(
                customer=request.user.customer,
                service=service,
                address=form.cleaned_data['address'],
                service_time=service_time,
                cost=service.price_hour * service_time,
            )
            return redirect('customer_profile', name=request.user.username)
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {'form': form, 'service': service})


@login_required
def rate_service(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    if not request.user.is_customer or service_request.customer.user_id != request.user.id:
        return redirect('customer_profile', name=request.user.username)

    if request.method == 'POST':
        form = RateServiceRequestForm(request.POST)
        if form.is_valid():
            service_request.rating = int(form.cleaned_data['rating'])
            service_request.save(update_fields=['rating'])
            _recompute_ratings(service_request.service)

    return redirect('customer_profile', name=request.user.username)
