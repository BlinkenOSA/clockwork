from rest_framework import serializers
from container.models import Container


class ContainerDigitizedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['barcode', 'digital_version_exists', 'technical_metadata']