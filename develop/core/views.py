from django.contrib.sites.models import Site
from django.urls import reverse
from django.views.generic.edit import FormView
from siteconfigs.models import SiteConfigModel
from .config import ExampleClass
from .forms import ExampleForm

class ExampleView(FormView):
    template_name = "core/example.html"
    form_class = ExampleForm

    def form_valid(self, form):
        result = super().form_valid(form)
        site = Site.objects.get_current()
        config, created = SiteConfigModel.objects.get_or_create(site=site, key="core.config.ExampleClass")
        config.value = {
            "example": form.cleaned_data["example"]
        }
        config.save()
        return result

    def get_success_url(self):
        return reverse("core-example")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["val"] = ExampleClass().get_key_value()
        return context
