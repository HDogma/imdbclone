from django.apps import AppConfig
from watson import search as watson


class MainConfig(AppConfig):
    name = 'main'

    @watson.update_index()
    def ready(self):
        Movies = self.get_model("Movies")
        watson.register(Movies, fields=("name", "description"))