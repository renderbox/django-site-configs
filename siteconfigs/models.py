# import uuid

# from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.text import slugify

# from django.urls import reverse
from django.contrib.sites.models import Site


class SettingType(models.IntegerChoices):
    COMMON = 1, _("Common")
    RESPONSE_META_TAG = 2, _("Response Meta Tag")


class SiteConfigKeyModel(models.Model):
    label = models.CharField(_("Key Label"), max_length=120, blank=False, unique=True)
    key = models.SlugField(_("Key"), blank=True, editable=False, unique=True)
    schema = models.JSONField(_("Schema"), default=dict, null=True, blank=True)
    deleted = models.BooleanField(
        _("Deleted"), default=False, help_text=_("Soft Deleted?")
    )
    multiples = models.BooleanField(
        _("Multiples"), help_text=_("Are multiple setting values allowed?")
    )
    admin_only = models.BooleanField(
        _("Django Admin Only"),
        help_text=_("Are these only editable by people with Django Admin privilages?"),
    )
    setting_type = models.IntegerField(
        _("Setting Type"), choices=SettingType.choices, blank=False, null=False
    )

    class Meta:
        verbose_name = _("Site Setting Key")
        verbose_name_plural = _("Site Setting Keys")

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        self.key = slugify(self.label)
        super().save(*args, **kwargs)


class SiteConfigModel(models.Model):
    key = models.ForeignKey(
        SiteConfigKeyModel,
        verbose_name=_("Site Setting Key Name"),
        on_delete=models.CASCADE,
        help_text=_("What setting is this value for?"),
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="settings",
    )  # This uses a callable so it will not trigger a migration with the projects it's included in
    deleted = models.BooleanField(
        _("Deleted"), default=False, help_text=_("Soft Delete the Setting value")
    )
    value = models.JSONField(_("Value"), default=dict)

    # TODO: Create manager to get record by key slug

    class Meta:
        verbose_name = _("Site Setting")
        verbose_name_plural = _("Site Settings")

    def __str__(self):
        return "{key} ({site}): {value}".format(
            key=self.key.key, site=self.site.name, value=str(self.value)
        )
