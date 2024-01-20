from abc import ABC, abstractmethod
from productsapp.models import Slider
from django.db.models import QuerySet


class SliderInterface(ABC):

    @abstractmethod
    def get_all(self) -> QuerySet[Slider]:
        """ Метод для получения всех слайдеров """
        pass
