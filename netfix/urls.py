"""netfix URL Configuration"""
from django.contrib import admin
from django.urls import include, path

from users import views as users_v
from . import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('services/', include('services.urls')),
    path('register/', include('users.urls')),
    path('login/', users_v.LoginUserView, name='login_user'),
    path('customer/<slug:name>/', v.customer_profile, name='customer_profile'),
    path('company/<slug:name>/', v.company_profile, name='company_profile'),
]
