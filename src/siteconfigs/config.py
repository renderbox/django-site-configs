# from re import S
from django.conf import settings as django_settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

from .models import SiteConfigModel

# get this from a django settings file if it's set, otherwise default to a value
SITE_CONFIG_NAME = getattr(
    django_settings, "DJANGO_SITE_CONFIGS_SITE_CONFIG_NAME", "default"
)


class SiteConfigBaseClass:
    _key = None
    _label = None
    _site = None
    _form_class = None  # convenience for the form class
    _is_superuser_config = False

    def __init__(self, site=None):

        if not site:
            # get the current site without needing to pass it in
            site = Site.objects.get_current()

        self._site = site

        site_conf, created = SiteConfigModel.objects.get_or_create(
            site=self._site, key=SITE_CONFIG_NAME
        )

        if created:  # if the site config is new, save the default values and return
            self.save()
            return

        config_name = self.get_config_name()

        if config_name in site_conf.value:
            # read in the data dictionary
            data = site_conf.value[config_name]["data"]
            # set the attributes of this instance
            for k, v in data.items():
                setattr(self, k, v)

            if "superuser" in site_conf.value[config_name]:
                self._is_superuser_config = site_conf.value[config_name]["superuser"]

        # read in each of the values and set the attribute of this instance if they exist
        for k, v in site_conf.value.items():
            setattr(self, k, v)

    def get_config_name(self):
        return ".".join([self.__class__.__module__, self.__class__.__name__])

    def get_label(self):
        return self._label

    def get_form(self):
        if self._form_class:
            return self._form_class
        return None

    def save(self):

        config, created = SiteConfigModel.objects.get_or_create(
            site=self._site, key=SITE_CONFIG_NAME
        )

        # get the full module path name for the instance
        config_name = self.get_config_name()

        # get all the attributes of this instance as a dictionary
        data = {
            attr: getattr(self, attr)
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("_")
        }

        # if the config name is not in the value dictionary, add it
        if config_name not in config.value:
            config.value[config_name] = {}

        # update the data dictionary with the new data
        if "data" not in config.value[config_name]:
            config.value[config_name]["data"] = data
        else:
            config.value[config_name]["data"].update(data)

        # print(config.value)

        config.save()

    def delete(self):
        """Delete the individual config from the site configs"""

        try:
            config = SiteConfigModel.objects.get(site=self._site, key=SITE_CONFIG_NAME)

        except ObjectDoesNotExist:  # if there is nothing to delete, exit early
            return

        config_name = self.get_config_name()

        if config_name in config.value:
            del config.value[config_name]
            config.save()
