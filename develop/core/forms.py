from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site

from .config import ExampleClass


class ExampleForm(forms.Form):
    example = forms.CharField(label=_("Example"), required=False, widget=forms.TextInput(attrs={"placeholder": _("Enter value")}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = ExampleClass().get_key_value()
        self.fields["example"].initial = initial.get("example")
