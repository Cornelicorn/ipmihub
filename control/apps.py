from django.apps import AppConfig
from ipmihub.env import refresh_interval

class ControlConfig(AppConfig):
    name = 'control'

    def ready(self):
        if refresh_interval != -1:
            # Import here as apps aren't loaded before
            from control.schedule import runner
            runner.start()
