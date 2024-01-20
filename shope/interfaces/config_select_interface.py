from abc import ABC, abstractmethod


class ConfigSelectInterface(ABC):

    @abstractmethod
    def get_config_value_by_name(self, name):
        """Получить значение конфигурации по названию"""
        pass
