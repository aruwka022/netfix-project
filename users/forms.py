from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = "date"


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(f"{value} is already taken.")


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])
    birth = forms.DateField(widget=DateInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "birth", "password1", "password2")

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_customer = True

        if commit:
            user.save()

            Customer.objects.create(
                user=user,
                birth=self.cleaned_data["birth"]
            )

        return user


class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])

    field = forms.ChoiceField(
        choices=Company._meta.get_field("field").choices
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "field", "password1", "password2")

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_company = True

        if commit:
            user.save()

            Company.objects.create(
                user=user,
                field=self.cleaned_data["field"]
            )

        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Email",
                "autocomplete": "off",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter Password"}
        )
    )