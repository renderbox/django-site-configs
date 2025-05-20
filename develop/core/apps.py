from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"
    configs = ["core.config.ExampleClass"]
