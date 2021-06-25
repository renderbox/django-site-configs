from django.views.generic import TemplateView

class SiteSettingsIndexView(TemplateView):
    template_name = "sitesettings/index.html"
