from django.db import IntegrityError
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
        sfield = self.schema.fields.create(field_class='CharField',
                                           field_name='name',
                                           required=True)

        qs = ['<SchemaField: SchemaField for {}: "{}">'.format(
            self.SCHEMA_TITLE,
            sfield.field_name)]

        self.assertQuerysetEqual(
            self.schema.fields.all(),
            qs)

    def test_schemafield_integrity(self):
        self.schema.fields.create(field_class='CharField',
                                  field_name='name',
                                  required=True)

        # lets try to create field with a name that already exists
        with self.assertRaises(IntegrityError):
            self.schema.fields.create(field_class='CharField',
                                      field_name='name',
                                      required=True)
