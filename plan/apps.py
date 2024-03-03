from django.apps import AppConfig


class PlanAppConfig(AppConfig):
    name = 'plan'

    def ready(self):
        import plan.signals
