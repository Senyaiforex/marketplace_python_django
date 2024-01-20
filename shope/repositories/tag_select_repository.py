from interfaces.tag_select_interface import TagSelectInterface
from django.db.models import QuerySet
from taggit.models import Tag


class TagSelectRepository(TagSelectInterface):

    def get_all_tags(self) -> QuerySet[Tag]:
        """Получить список всех тегов"""
        return Tag.objects.all()
