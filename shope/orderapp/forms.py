from django import forms
from orderapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('fio', 'phone_number', 'city', 'address', 'delivery_type')
        widgets = {'delivery_type': forms.RadioSelect(),
                   'address': forms.Textarea()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fio'].required = True
        self.fields['fio'].widget.attrs['class'] = 'form-input'
        self.fields['phone_number'].required = True
        self.fields['phone_number'].widget.attrs['class'] = 'form-input'
        self.fields['phone_number'].widget.attrs[
            'placeholder'] = '+79991112233'
        self.fields['city'].required = True
        self.fields['city'].widget.attrs['class'] = 'form-input'
        self.fields['address'].required = True
        self.fields['address'].widget.attrs['class'] = 'form-textarea'
        self.fields['address'].widget.attrs['autocomplete'] = 'on'
        for name, field in self.fields.items():
            field.widget.attrs['id'] = name
            field.widget.attrs['data-validate'] = 'require'
