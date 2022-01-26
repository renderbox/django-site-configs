from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from siteconfigs.config import SiteConfigBaseClass
from .forms import ExampleForm

class ExampleClass(SiteConfigBaseClass):
    label = _("Example")
    default = {"example": "Default Value"}
    form_class = ExampleForm
    
    def __init__(self):
        site = Site.objects.get_current()
        self.key = ".".join([__name__, __class__.__name__])
        super().__init__(site, self.key)
