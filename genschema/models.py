from django.db import models


class Schema(models.Model):
    title = models.CharField(unique=True, max_length=20)


class SchemaField(models.Model):
    schema = models.ForeignKey('Schema', on_delete=models.CASCADE,
                               related_name='fields')

    field_class = models.CharField(max_length=50)

    # Make this slugified
    field_name = models.SlugField(max_length=10)

    required = models.BooleanField(default=True)

    class Meta:
        unique_together = ('schema', 'field_name', )

    def __str__(self):
        return 'SchemaField for {}: "{}"'.format(self.schema.title,
                                                 self.field_name)


class SchemaInstance(models.Model):
    schema = models.ForeignKey('Schema', on_delete=models.CASCADE)


class SchemaIValue(models.Model):
    schemainstance = models.ForeignKey('SchemaInstance',
                                       on_delete=models.CASCADE)
    schemafield = models.ForeignKey('SchemaField',
                                    on_delete=models.CASCADE)
    fieldvalue = models.TextField()

    class Meta:
        unique_together = ('schemainstance', 'schemafield')
        ordering = ('schemainstance', 'schemafield', )

    def __str__(self):
        return 'SchemaIValue for "{}" => {}'.format(
            self.schemafield.field_name,
            self.fieldvalue)

