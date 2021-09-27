from django.core.exceptions import ObjectDoesNotExist
from .models import SiteConfigModel

class SiteConfigBaseClass():
    key = None
    label = None
    site = None
    instance = None
    value = dict()
    default = dict()
    form_class = None
    is_superuser_config = False

    def __init__(self, site, key):
        self.site = site
        try:
            site_conf = SiteConfigModel.objects.get(site=site, key=key)
            self.instance = site_conf
            self.value = site_conf.value
        except ObjectDoesNotExist:
            pass

    def get_key_value(self):
        if self.value:
            return self.value
        return self.default

    def save(self, data, value_key):
        config, created = SiteConfigModel.objects.get_or_create(site=self.site, key=self.key)
        config.value = {
            value_key: data
        }
        config.save()
        self.instance = config
        self.value = config.value

    def delete(self):
        if self.instance:
            self.instance.delete()
            self.instance = None
            self.value = dict()

    
