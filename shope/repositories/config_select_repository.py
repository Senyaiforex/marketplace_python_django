from interfaces import ConfigSelectInterface
from coreapp.models import ConfigModel


class ConfigSelectRepository(ConfigSelectInterface):

    def get_config_value_by_name(self, name):
        """Получить значение конфигурации по названию"""
        return ConfigModel.objects.filter(name=name).first().value
