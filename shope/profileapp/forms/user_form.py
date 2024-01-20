from django import forms
from authapp.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
