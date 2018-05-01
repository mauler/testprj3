from django import forms
from django.test import TestCase

from genschema.handler import Handler
from genschema.models import Schema, SchemaInstance


class HandlerTests(TestCase):

    def setUp(self):
        self.schema = Schema.objects.create(title='My schema')

        self.schema.fields.create(field_name='name',
                                  field_class='django.forms.CharField')

        self.schema.fields.create(field_name='age',
                                  field_class='django.forms.IntegerField')

    def test_save(self):

        # is this a MOCK ?
        class SchemaInstanceForm(forms.ModelForm):
            name = forms.CharField()
            age = forms.IntegerField()

            class Meta:
                fields = ['schema', 'name', 'age']
                model = SchemaInstance

        form = SchemaInstanceForm({'name': 'Paulo',
                                   'age': '10',
                                   'schema': self.schema.id})

        # lets populate the cleaned data
        form.is_valid()
        schemainstance = form.save()

        self.handler = Handler(self.schema, form.cleaned_data, schemainstance)
        schemainstance = self.handler.save()

        self.assertQuerysetEqual(
            schemainstance.schemaivalue_set.all(),
            ['<SchemaIValue: SchemaIValue for "name" => "Paulo">',
            '<SchemaIValue: SchemaIValue for "age" => 10>'])
