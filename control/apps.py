from django.apps import AppConfig


class ControlConfig(AppConfig):
    name = 'control'

    def ready(self):
        from control.schedule import runner
        runner.start()
