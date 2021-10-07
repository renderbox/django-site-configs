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
        if form.cleaned_data["example"]:
            ExampleClass().save(form.cleaned_data["example"], "example")
        else:
            ExampleClass().delete()
        return result

    def get_success_url(self):
        return reverse("core-example")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        config = ExampleClass()
        val = config.get_key_value("example")
        context["form"] = config.form_class(initial={"example": val})
        context["val"] = val
        return context
