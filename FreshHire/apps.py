from django.apps import AppConfig


class FreshhireConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FreshHire'
    def ready(self):
     import FreshHire.signals