from django.urls import path

from sitesettings import views

urlpatterns = [
    path("", views.SiteSettingsIndexView.as_view(), name="sitesettings-index"),
]
