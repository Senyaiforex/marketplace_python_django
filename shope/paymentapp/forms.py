from django import forms
from django.utils.translation import gettext_lazy as _


class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=19,
        min_length=13,
        required=True,
        label=_('Card number'))
    card_holder = forms.CharField(
        max_length=30,
        required=True,
        label=_('Cardholder name'))
    expiry_date = forms.DateField(
        required=True,
        input_formats=['%m/%y',],
        widget=forms.DateInput,
        label=_('Expiry date'))
    cvv = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.PasswordInput,
        label=_('Code'))
    total_sum = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.HiddenInput,
        label=_('total sum (rub.)'),
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['expiry_date'].widget.attrs['placeholder'] = _('MM/YY')
        self.fields['expiry_date'].widget.attrs['class'] = 'input_small'
        self.fields['cvv'].widget.attrs['placeholder'] = 'CVV'
        self.fields['cvv'].widget.attrs['class'] = 'input_small'
