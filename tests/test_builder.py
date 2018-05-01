from django import forms
from django.test import TestCase

from genschema.builder import Builder
from genschema.models import Schema


class BuilderTests(TestCase):
    SCHEMA_TITLE = 'My Schema'

    def setUp(self):
        self.schema = Schema.objects.create(title=self.SCHEMA_TITLE)
        self.builder = Builder(self.schema)

    def test_make_class_name(self):
        self.assertEqual(self.builder._make_class_name('Paulo Form Test'),
                         'PauloFormTestForm')

    def test_make_field_validation(self):
        """ Make sure field_class has a namespace to be imported. """
        with self.assertRaises(ValueError):
            self.builder._make_field('CharField', False)

    def test_make_field(self):
        field = self.builder._make_field('django.forms.CharField', False)
        self.assertIsInstance(field, forms.CharField)
        self.assertFalse(field.required)

    def test_make_fields(self):
        fields = (
            {'field_name': 'age',
             'field_class': 'django.forms.IntegerField',
             'required': True},
        )
        collection = self.builder._make_fields(fields)
        self.assertIn('age', collection)

    def test_make_form_class(self):
        form_class = self.builder._make_form_class(
            'PauloForm',
            {'age': forms.IntegerField()})

        self.assertTrue(issubclass(form_class, forms.ModelForm))
        self.assertEqual(form_class.Meta.fields, ['schema', 'age'])
