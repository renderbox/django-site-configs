[![Python Tests](https://github.com/renderbox/django-site-configs/actions/workflows/python-test.yml/badge.svg)](https://github.com/renderbox/django-site-configs/actions/workflows/python-test.yml)

[![Publish Python distribution to PyPI](https://github.com/renderbox/django-site-configs/actions/workflows/python-publish.yml/badge.svg)](https://github.com/renderbox/django-site-configs/actions/workflows/python-publish.yml)

# Django Site Configs

Django Site Configs stores small, structured configuration objects per Django
site. It uses `django.contrib.sites` to choose the active site and stores all
config objects for that site in one `SiteConfigModel.value` JSON field.

The package is intended for project or app settings that should live in the
database instead of in `settings.py`, while still being represented in Python as
simple classes with defaults and optional form classes.

## Requirements

- Python 3.10+
- Django 5.2 or Django 6.0
- `django.contrib.sites`

The package dependency range is currently:

```toml
django>=5.2,<6.1
```

## Installation

Install the package, then add the sites framework and `siteconfigs` to
`INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    "django.contrib.sites",
    "siteconfigs",
]

SITE_ID = 1
```

Run migrations:

```bash
python manage.py migrate
```

The model is registered with the Django admin as `Site Setting`.

## Defining A Config

Create a class that subclasses `SiteConfigBaseClass`. Public class attributes
become default config values.

```python
from django import forms
from django.utils.translation import gettext_lazy as _
from siteconfigs.config import SiteConfigBaseClass


class FeatureFlagsForm(forms.Form):
    show_banner = forms.BooleanField(required=False)


class FeatureFlags(SiteConfigBaseClass):
    _label = _("Feature flags")
    _form_class = FeatureFlagsForm

    show_banner = False
```

Instantiate the class to load values for the current site:

```python
flags = FeatureFlags()

if flags.show_banner:
    ...
```

Pass a `Site` instance to load or save config for a specific site:

```python
from django.contrib.sites.models import Site

site = Site.objects.get(domain="example.com")
flags = FeatureFlags(site=site)
```

## Saving Values

Set attributes on the config object and call `save()`.

```python
flags = FeatureFlags()
flags.show_banner = True
flags.save()
```

Calling `delete()` removes only that config class's data from the site's JSON
record. It does not delete the `SiteConfigModel` row.

```python
FeatureFlags().delete()
```

## Optional Forms

If a config class sets `_form_class`, `get_form()` returns that form class.
This is useful when building custom admin or project views around a config.

```python
config = FeatureFlags()
form_class = config.get_form()
form = form_class(initial={"show_banner": config.show_banner})
```

## Storage Format

For each site, the package creates or updates one `SiteConfigModel` row with:

- `site`: the Django `Site`
- `key`: the config namespace, defaulting to `"default"`
- `value`: a JSON object keyed by each config class's full import path

Example `value`:

```json
{
  "myapp.config.FeatureFlags": {
    "data": {
      "show_banner": true
    }
  }
}
```

The namespace stored in `SiteConfigModel.key` can be changed with:

```python
DJANGO_SITE_CONFIGS_SITE_CONFIG_NAME = "staging"
```

This lets one site have multiple named config records, such as `default` and
`staging`.

## Current Behavior And Limits

- The current site is resolved with `Site.objects.get_current()` when no site is
  passed to the config class.
- Config values are plain JSON-serializable public attributes.
- Saving includes all non-callable public attributes on the config instance.
- The package provides the storage model and base class, but not a generic UI
  for editing every config class.
- The `deleted` field on `SiteConfigModel` is available for project-level soft
  delete workflows, but `SiteConfigBaseClass.delete()` removes the config data
  from the JSON value directly.

## Development

Install test dependencies and run the test suite:

```bash
python -m pip install -e ".[test]"
python -m pytest src/siteconfigs develop
```

Check for missing migrations:

```bash
python develop/manage.py makemigrations --check --dry-run
```
