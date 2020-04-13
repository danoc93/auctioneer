from rest_framework import serializers


class CustomFieldsModelSerializer(serializers.ModelSerializer):
    """
    A Custom Serializer to allow field overriding.
    Good for creating dynamic views without the need of an additional entity layer.
    https://stackoverflow.com/questions/53319787/how-can-i-select-specific-fields-in-django-rest-framework
    """
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is None:
            return

        allowed = set(fields)
        existing = set(self.fields.keys())
        for field_name in existing - allowed:
            self.fields.pop(field_name)
