from abc import ABC, abstractmethod

from django.db.models import QuerySet

from authapp.models import User
from profileapp.models import Profile


class ProfileInterface(ABC):

    @abstractmethod
    def get_profile(self, user: User) -> Profile:
        """ Метод для получения объекта Profile по user """
        pass

    def get_profile_by_phone_number(self, phone_number):
        """ Метод для проверки уникальности номера телефона"""
        pass

    def get_profile_by_superuser(self) -> QuerySet[Profile]:
        """ Метод для получения всех админов """
        pass
