from django import forms
from profileapp.models import Profile
from django.core.exceptions import ValidationError
from django.conf import settings
from phonenumber_field.formfields import PhoneNumberField
from repositories.profile_repository import ProfileRepository
from django.utils.translation import gettext_lazy as _

profile_rep = ProfileRepository()


class ProfileForm(forms.ModelForm):
    avatar_image = forms.ImageField(
        widget=forms.widgets.ClearableFileInput
    )
    phone_number = PhoneNumberField(
        initial='+7',
        widget=forms.TextInput(
            attrs={
                "class": 'form-input',
                'placeholder': '+71231231212'
            }
        )
    )
    phone_number.error_messages['invalid'] = _(
        'Enter a valid phone number (e.g. +79998887766)'
    )

    class Meta:
        model = Profile
        fields = ('fio', 'avatar_image', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar_image'].required = False
        self.fields['fio'].required = True
        self.fields['phone_number'].required = False

    def clean_avatar_image(self):
        data = self.cleaned_data["avatar_image"]
        if data:
            if data.size > settings.MAX_AVATAR_IMAGE_SIZE:
                raise ValidationError(_("Maximum avatar size is 2 Mb"))
        return data

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        saved_profile = profile_rep.get_profile_by_phone_number(
            phone_number=phone_number
        )
        if saved_profile and phone_number != self.instance.phone_number:
            raise ValidationError(_('This phone number is already in use'))
        return phone_number
