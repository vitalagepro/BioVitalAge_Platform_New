from django.apps import AppConfig # type: ignore


class BiovitalageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BioVitalAge'

    def ready(self):
        # qui importiamo il modulo signals
        import BioVitalAge.signals