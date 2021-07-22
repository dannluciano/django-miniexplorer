from django.apps import AppConfig


class MiniexplorerConfig(AppConfig):
    name = 'miniexplorer'
    verbose_name = 'SQL Explorer'
    
    default_auto_field = 'django.db.models.AutoField'
