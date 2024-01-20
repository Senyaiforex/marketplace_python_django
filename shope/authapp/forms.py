from django import forms
from authapp.models import User
from django.contrib.auth.forms import AuthenticationForm, \
    UserCreationForm, UsernameField, SetPasswordForm, \
    PasswordResetForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from .tasks import send_link_for_password


class UserLoginForm(AuthenticationForm):
    """
    Форма для авторизации пользователя
    """
    username = UsernameField(
        widget=forms.TextInput(
            attrs={"autofocus": True,
                   "placeholder": "e-mail"
                   })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.
        PasswordInput(
            attrs={"autocomplete": "current-password",
                   "placeholder": "********"
                   })
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        """
        Переопределение метода для отображения ошибки при неактивном
        пользователе
        """
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                try:  # попытка найти пользователя с таким email
                    user_not_active = User.objects.get(email=username)
                except ObjectDoesNotExist:
                    user_not_active = None
                if user_not_active is not None and \
                        user_not_active.check_password(password):
                    # если пользователь с таким username(email) существует,
                    # и введён верный пароль, но его учетная запись неактивна
                    self.confirm_login_allowed(user_not_active)
                else:
                    raise self.get_invalid_login_error()
        return self.cleaned_data


class UserSignUpForm(UserCreationForm):
    """
    Форма для регистрации пользователя
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = _('Password')
        self.fields['password2'].widget. \
            attrs['placeholder'] = _('Password confirmation')
        self.fields['first_name'].widget.attrs['placeholder'] = _('Name')
        self.fields['last_name'].widget.attrs['placeholder'] = _('Surname')
        self.fields['middle_name'].widget.attrs['placeholder'] = _('Middle name')  # noqa
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        for name_field, field in self.fields.items():
            field.widget.attrs['class'] = 'user-input'

    class Meta:
        model = User
        fields = ('email', 'first_name',
                  'middle_name', 'last_name')


class UserResetPasswordForm(PasswordResetForm):
    """
    Форма для ввода email
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'

    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None,
    ):
        """
        Метод для отправки сообщения на e-mail
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Тема письма не должна содержать новых строк
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        html_email = loader.render_to_string(html_email_template_name, context)
        send_link_for_password.delay(
            subject, body,
            from_email, to_email, html_email
        )  # отправка сообщения на e-mail


class UserSetPasswordForm(SetPasswordForm):
    """
    Форма для ввода нового пароля
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['placeholder'] = _('Password')  # noqa
        self.fields['new_password2'].widget. \
            attrs['placeholder'] = _('Password confirmation')
