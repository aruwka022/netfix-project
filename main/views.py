from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth import logout as django_logout

from services.models import Service


def home(request):
    most_requested = Service.objects.annotate(
        num_requests=Count('requests')
    ).order_by('-num_requests', '-date')[:6]

    return render(request, "main/home.html", {"services": most_requested})


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
