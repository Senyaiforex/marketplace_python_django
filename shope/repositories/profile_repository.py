from django.db.models import QuerySet

from authapp.models import User
from interfaces.profile_interface import ProfileInterface
from profileapp.models import Profile


class ProfileRepository(ProfileInterface):
    def get_profile(self, user: User) -> Profile:
        return Profile.objects.get(user=user)

    def get_profile_by_phone_number(self, phone_number):
        return Profile.objects.filter(phone_number=phone_number).first()

    def get_profile_by_superuser(self) -> QuerySet[Profile]:
        return Profile.objects.filter(user__is_superuser=True)
