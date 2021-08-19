from django.test import Client, TestCase
from django.urls import reverse
from core.config import ExampleClass
from .models import SiteConfigModel

class ExampleTests(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_default_value(self):
        default = ExampleClass().get_key_value()
        self.assertEquals(default, {"example": "Default Value"})

    def test_create_config(self):
        self.assertEqual(SiteConfigModel.objects.count(), 0)
        uri = reverse("core-example")
        response = self.client.post(uri, {"example": "Testing"})
        self.assertEqual(SiteConfigModel.objects.count(), 1)
        config = SiteConfigModel.objects.first()
        self.assertEqual(config.key, "core.config.ExampleClass")
        self.assertEqual(config.value, {"example": "Testing"})
        self.assertEqual(config.value, ExampleClass().get_key_value())
