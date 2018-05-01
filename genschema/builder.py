from importlib import import_module

from django import forms

from genschema.models import SchemaInstance


class Builder:
    """ Here I would like to describe the basic BUSINESS RULE here"""

    def __init__(self, schema):
        """ Here I do sphinx based comments, in this phrase just things useful
        about the parameters itself, not the business rule.

        :param schema: The Schema instance to have the form built.
        :type schema: class:schema.models.Schema
        """
        self._schema = schema

    @classmethod
    def _make_class_name(cls, title):
        """ Isnt't over thinking, it's just easy to write TDD stuff."""
        class_name = '{}Form'.format(title.title().replace(' ', ''))
        return class_name

    @classmethod
    def _make_field(cls, field_class, required):
        parts = field_class.split('.')

        if len(parts) < 2:
            # No message :)
            raise ValueError

        field_part = parts[-1]
        field_namespace = '.'.join(parts[:-1])

        module = import_module(field_namespace)
        field_class = getattr(module, field_part)

        field = field_class(required=required)

        return field

    @classmethod
    def _make_fields(cls, fields):
        """ No DATABASE here, just simple python objects. Easily to write TDD
        tests. """

        collection = {}
        for field in fields:
            field_instance = cls._make_field(field['field_class'],
                                             field['required'])

            collection[field['field_name']] = field_instance
        return collection

    @classmethod
    def _make_form_class(cls, class_name, class_attrs):

        class Meta:
            model = SchemaInstance
            fields = ['schema'] + list(class_attrs.keys())

        class_attrs['Meta'] = Meta
        form_class = type(class_name, (forms.ModelForm, ), class_attrs)

        return form_class

    def get_form_class(self):
        """ No Comments here, check the description ABOVE. """

        attrs = self._make_fields(list(self._schema.fields.values()))

        class_name = self._make_class_name(self._schema.title)

        form_class = self._make_class(class_name, attrs)

        return form_class
