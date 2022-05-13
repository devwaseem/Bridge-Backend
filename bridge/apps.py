from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BridgeConfig(AppConfig):
    name = "bridge"
    verbose_name = _("Bridge")

    def ready(self):
        try:
            import bridge.signals  # noqa F401
        except ImportError:
            pass
