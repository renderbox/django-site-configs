from django.core.exceptions import ObjectDoesNotExist
from .models import SiteConfigModel

class SiteConfigBaseClass():
    label = None
    value = dict()
    default = dict()
    is_superuser_config = False
    site = None

    def __init__(self, site, key):
        self.site = site
        try:
            site_conf = SiteConfigModel.objects.get(site=site, key=key)
            self.value = site_conf.value
        except ObjectDoesNotExist:
            pass

    def get_key_value(self):
        if self.value:
            return self.value
        return self.default
