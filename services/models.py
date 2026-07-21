from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import Company, Customer, FIELD_CHOICES

SERVICE_FIELD_CHOICES = tuple(
    choice for choice in FIELD_CHOICES if choice[0] != 'All in One'
)


class Service(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(5)], default=0)
    field = models.CharField(max_length=30, blank=False,
                              null=False, choices=SERVICE_FIELD_CHOICES)
    date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='requests')
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='requests')
    address = models.CharField(max_length=100)
    service_time = models.DecimalField(decimal_places=2, max_digits=6)
    cost = models.DecimalField(decimal_places=2, max_digits=100)
    request_date = models.DateTimeField(auto_now_add=True, null=False)
    rating = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.customer} requested {self.service}"
