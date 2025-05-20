from core.config import ExampleClass  # loaded with the Django app
from django.test import Client, TestCase
from django.urls import reverse

from .models import SiteConfigModel


class ExampleTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_default_value(self):
        default = ExampleClass()
        self.assertEqual(default.example, "Default Value")

    def test_create_config(self):
        """Test that a config is created when called if it's missing"""
        self.assertEqual(SiteConfigModel.objects.count(), 0)
        uri = reverse("core-example")
        response = self.client.post(uri, {"example": "Testing"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SiteConfigModel.objects.count(), 1)
        config = SiteConfigModel.objects.last()
        self.assertEqual(config.key, "default")
        self.assertEqual(
            config.value, {"core.config.ExampleClass": {"data": {"example": "Testing"}}}
        )

    def test_adding_dynamic_attribute(self):
        example = ExampleClass()
        example.new_value = "test_key"
        example.save()

        setting = SiteConfigModel.objects.last()

        self.assertEqual(
            setting.value,
            {
                "core.config.ExampleClass": {
                    "data": {"example": "Default Value", "new_value": "test_key"}
                }
            },
        )

    # need a test that will show it loading a value from the database
    def test_loading_data(self):
        """
        A test that will show it loading a value from the database
        """
        example = ExampleClass()
        example.example = "Testing"
        example.save()

        example_two = ExampleClass()
        self.assertEqual(example_two.example, "Testing")

    def test_delete(self):
        """Test that a config is removed when called"""
        ExampleClass().save()
        self.assertEqual(SiteConfigModel.objects.count(), 1)
        self.assertEqual(
            SiteConfigModel.objects.last().value,
            {"core.config.ExampleClass": {"data": {"example": "Default Value"}}},
        )
        # check the value in the database

        ExampleClass().delete()
        self.assertEqual(SiteConfigModel.objects.count(), 1)
        # check that the config is removed from the SiteConfig model
        self.assertEqual(
            SiteConfigModel.objects.last().value,
            {},
        )
