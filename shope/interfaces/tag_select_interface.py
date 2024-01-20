from abc import ABC, abstractmethod
from django.db.models import QuerySet
from taggit.models import Tag


class TagSelectInterface(ABC):

    @abstractmethod
    def get_all_tags(self) -> QuerySet[Tag]:
        """Получить список всех тегов"""
        pass
