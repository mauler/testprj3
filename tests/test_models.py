from django.test import TestCase

from genschema.models import Schema


class BaseTest(TestCase):
    SCHEMA_TITLE = 'My Schema'


class SchemaTests(BaseTest):

    def test_schema(self):
        schema = Schema(title=self.SCHEMA_TITLE)
        schema.save()
        self.assertEqual(schema.title, self.SCHEMA_TITLE)


class SchemaFieldTests(BaseTest):

    def setUp(self):
        self.schema = Schema.objects.create(title=self.SCHEMA_TITLE)

    def test_schemafield(self):
        pass
