from django.contrib import admin

# Register your models here.
from .models import SiteConfigKeyModel, SiteConfigModel


class SiteConfigKeyModelAdmin(admin.ModelAdmin):
    readonly_fields = ["key"]


class SiteConfigModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(SiteConfigKeyModel, SiteConfigKeyModelAdmin)
admin.site.register(SiteConfigModel, SiteConfigModelAdmin)
