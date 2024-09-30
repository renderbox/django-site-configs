from django.contrib import admin
from .models import SiteConfigModel


class SiteConfigModelAdmin(admin.ModelAdmin):
    list_display = ["key", "site"]
    search_fields = ["key", "site__name"]


admin.site.register(SiteConfigModel, SiteConfigModelAdmin)
