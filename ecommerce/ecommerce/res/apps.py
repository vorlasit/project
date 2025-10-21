from django.apps import AppConfig


class ResConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'res'
    
    def ready(self):
        import res.signals