from rest_framework import serializers
from container.models import Container


class ContainerDigitizedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['barcode', 'digital_version_exists', 'digital_version_technical_metadata', 'digital_version_creation_date']