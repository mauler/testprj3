from django.db import models


class Schema(models.Model):
    title = models.CharField(unique=True, max_length=20)


class SchemaField(models.Model):
    schema = models.ForeignKey('Schema', on_delete=models.CASCADE)

    field_class = models.CharField(max_length=50)

    # Make this slugified
    field_name = models.SlugField(max_length=10)

    required = models.BooleanField(default=True)

    class Meta:
        unique_together = ('schema', 'field_name', )


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
