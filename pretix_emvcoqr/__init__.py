from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = '0.1.1'


class PluginApp(PluginConfig):
    name = 'pretix_emvcoqr'
    verbose_name = 'EMVCo QR Payment Plugin'

    class PretixPluginMeta:
        name = gettext_lazy('EMVCo QR Payment Plugin')
        author = 'Panawat Wong-klaew'
        description = gettext_lazy('Manual payment plugin with EMVCo QR Code')
        visible = True
        version = __version__
        category = 'PAYMENT'
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretix_emvcoqr.PluginApp'
