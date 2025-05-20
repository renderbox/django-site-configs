# Django Site Configs: Docs

Django site configs is designed allow a per-site config for a multi-site project.

## Project Goals:

- To have a generic universal setting file per site akin to the pyproject.toml allowing for third party packages to place their per-site config data in a common location.
- To have a cacheable resource to reduce DB hits and still be configured by the user.
- To have a config that can be edited user's and admins based on permissions.

These setting are created by the developer by subclassing the SiteConfigBaseClass() located in siteconfigs.config module.

There are a couple things that need to be updated with the package and after that we will revist the docs for more details. In the mean time, you can hit us up via [our issue tracker](https://github.com/renderbox/django-site-configs/issues) and will try to answer those questions more quickly.
