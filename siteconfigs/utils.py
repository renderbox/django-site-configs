# Utility to make sure to get the correct site object to use
from django.contrib.sites.models import Site


def get_current_site(request):
    if hasattr(request, "site"):
        current_site = request.site
    else:
        current_site = Site.objects.get_current()
    return current_site
