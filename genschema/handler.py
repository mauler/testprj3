from json import dumps


class Handler:
    """ Saves the form into the database. """

    def __init__(self, schema, cleaned_data, schema_instance=None):
        self._schema = schema
        self._cleaned_data = cleaned_data
        self._schema_instance = schema_instance

    def save(self):
        """ Writing/prototyping, NEEDS REFACTORY """
        sinstance = (self._schema_instance or
                     self._schema.schemainstance_set.create())
        fields = {i.field_name: i for i in self._schema.fields.all()}
        for k, v in self._cleaned_data.items():

            if k == 'schema':
                continue

            sivalue, created = fields[k].schemaivalue_set.get_or_create(
                schemainstance=sinstance,
                fieldvalue=dumps(self._cleaned_data[k]))
            if not created:
                sivalue.fieldvalue = dumps(v)
                sivalue.save(update_fields=['fieldvalue'])

        return sinstance
