from django import forms


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=6, min_value=0.01)
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, choices='', **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        if choices:
            self.fields['field'].choices = choices
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour (€)'


class RequestServiceForm(forms.Form):
    address = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Address', 'autocomplete': 'off'}))
    service_time = forms.DecimalField(
        decimal_places=2, max_digits=6, min_value=0.5,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Service Time (hours)'}))


RATING_CHOICES = [(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')]


class RateServiceRequestForm(forms.Form):
    rating = forms.ChoiceField(
        choices=RATING_CHOICES, widget=forms.RadioSelect, label='')
