from django.contrib import admin

# Register your models here.
from .models import SiteConfigModel

class SiteConfigModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(SiteConfigModel, SiteConfigModelAdmin)
