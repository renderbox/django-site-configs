from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.sites.models import Site


class SiteConfigModel(models.Model):
    """
    Config table for various packages and their configs.  The configs are consolidated in a JSON
    field on a per site basis.  This allows for a single table to store all configs for a site.

    It is possible to have multiple config records for a single site that can be switched based
    on a Django Config setting.  This is useful for having different configs for different parts
    of a site's deployment.  For example, a site could have a "default" setting and a "staging",
    each of which could have different configs and loaded based on the Django Config setting.
    """

    key = models.CharField(_("Key"), max_length=120, blank=False)  # Path to module
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="settings",
    )  # This uses a callable so it will not trigger a migration with the projects it's included in
    deleted = models.BooleanField(
        _("Deleted"), default=False, help_text=_("Soft Delete the Setting value")
    )
    value = models.JSONField(_("Value"), default=dict)

    class Meta:
        verbose_name = _("Site Setting")
        verbose_name_plural = _("Site Settings")
        constraints = [
            models.UniqueConstraint(fields=["key", "site"], name="unique key per site")
        ]

    def __str__(self):
        return "{key} ({site}): {value}".format(
            key=self.key, site=self.site.name, value=str(self.value)
        )
