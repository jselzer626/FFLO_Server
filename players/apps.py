from django.apps import AppConfig


class PlayersConfig(AppConfig):
    name = 'players'
    def ready(self):
        from scheduler import scheduler
        scheduler.start()
