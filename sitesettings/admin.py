from django.contrib import admin

# Register your models here.
from .models import SiteSettingKeyModel, SiteSettingModel


class SiteSettingKeyModelAdmin(admin.ModelAdmin):
    readonly_fields = ["key"]


class SiteSettingModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(SiteSettingKeyModel, SiteSettingKeyModelAdmin)
admin.site.register(SiteSettingModel, SiteSettingModelAdmin)
