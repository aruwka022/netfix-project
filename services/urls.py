from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.service_list, name='services_list'),
    path('create/', v.create, name='services_create'),
    path('requests/<int:request_id>/rate/', v.rate_service, name='rate_service'),
    path('<int:id>', v.index, name='index'),
    path('<int:id>/request_service/', v.request_service, name='request_service'),
    path('<int:id>/edit/', v.edit_service, name='edit_service'),
    path('<int:id>/delete/', v.delete_service, name='delete_service'),
    path('<slug:field>/', v.service_field, name='services_field'),
]
