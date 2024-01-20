from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from repositories import OrderRepository
from profileapp.forms import ProfileForm, UserForm, UserPasswordSetForm
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext_lazy as _

order_rep = OrderRepository()


class ProfileUpdateView(LoginRequiredMixin, View):
    """
    View-класс для обновления информации о пользователе
    """
    template_name = 'profileapp/profile.html'
    success_message = _('Profile is updated successfully')

    def get(self, request):
        context = {
            'user_form': UserForm(instance=self.request.user),
            'profile_form': ProfileForm(instance=self.request.user.profile),
            'password_form': UserPasswordSetForm(user=self.request.user)
        }

        return render(request, self.template_name, context)

    def post(self, request):
        profile_form = ProfileForm(request.POST,
                                   request.FILES,
                                   instance=self.request.user.profile)

        user_form = UserForm(request.POST,
                             instance=self.request.user)

        password_form = UserPasswordSetForm(data=request.POST,
                                            user=request.user)

        if all([profile_form.is_valid(),
                user_form.is_valid(),
                password_form.is_valid()]):

            profile_form.save()
            user_form.save()

            if password_form.has_changed():
                password_form.save()
                update_session_auth_hash(request, password_form.user)

            messages.success(request, self.success_message)
            return redirect(self.request.path)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form': password_form
        }

        return render(request, self.template_name, context=context)
