from django.apps import AppConfig


class SalesConfig(AppConfig):
    name = 'SALES'

    def ready(self):
        import SALES.signals
