from django import forms
from django.utils.translation import gettext_lazy as _


class ExampleForm(forms.Form):
    example = forms.CharField(label=_("Example"), required=False, widget=forms.TextInput(attrs={"placeholder": _("Enter value")}))
