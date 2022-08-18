from hashids import Hashids
from rest_framework import serializers
from isad.models import Isad


class ArchivalUnitsFullViewSerializer(serializers.ModelSerializer):
    title_original = serializers.SerializerMethodField()

    def get_title_original(self, obj):
        return obj.archival_unit.title_original

    class Meta:
        model = Isad
        fields = '_all_'

