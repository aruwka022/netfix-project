from datetime import date

from django.shortcuts import render, get_object_or_404

from users.models import User, Company, Customer
from services.models import ServiceRequest


def calculate_age(birth):
    today = date.today()
    return today.year - birth.year - (
        (today.month, today.day) < (birth.month, birth.day)
    )


def customer_profile(request, name):
    profile_user = get_object_or_404(User, username=name, is_customer=True)
    customer = get_object_or_404(Customer, user=profile_user)
    requests = customer.requests.all().order_by('-request_date')

    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'user_age': calculate_age(customer.birth),
        'requests': requests,
    })


def company_profile(request, name):
    profile_user = get_object_or_404(User, username=name, is_company=True)
    company = get_object_or_404(Company, user=profile_user)
    services = company.services.all().order_by("-date")

    context = {
        'profile_user': profile_user,
        'company': company,
        'services': services,
    }

    if request.user.is_authenticated and request.user.id == profile_user.id:
        context['incoming_requests'] = ServiceRequest.objects.filter(
            service__company=company
        ).select_related('service', 'customer__user').order_by('-request_date')

    return render(request, 'users/profile.html', context)
