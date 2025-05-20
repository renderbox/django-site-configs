from django.utils.translation import gettext_lazy as _
from siteconfigs.config import SiteConfigBaseClass
from .forms import ExampleForm


class ExampleClass(SiteConfigBaseClass):
    _label = _("Example")
    _form_class = ExampleForm
    example = "Default Value"
