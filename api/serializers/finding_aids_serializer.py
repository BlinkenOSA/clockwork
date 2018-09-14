from rest_framework import serializers

from archival_unit.models import ArchivalUnit
from finding_aids.models import FindingAidsEntity, FindingAidsEntityAlternativeTitle, FindingAidsEntityDate, \
    FindingAidsEntityCreator, FindingAidsEntityPlaceOfCreation, FindingAidsEntitySubject, \
    FindingAidsEntityAssociatedPerson, FindingAidsEntityAssociatedCorporation, FindingAidsEntityAssociatedCountry, \
    FindingAidsEntityAssociatedPlace, FindingAidsEntityLanguage


class ArchivalUnitSerializer(serializers.ModelSerializer):
    theme = serializers.StringRelatedField(many=True)
    level = serializers.SerializerMethodField()

    def get_level(self, value):
        if value == 'F':
            return 'Fonds'
        elif value == 'SF':
            return 'Subfonds'
        else:
            return 'Series'

    class Meta:
        model = ArchivalUnit
        exclude = ('sort', 'reference_code_id', 'parent')


class FindingAidsAlternativeTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindingAidsEntityAlternativeTitle
        exclude = ('id', 'fa_entity')


class FindingAidsEntityDateSerializer(serializers.ModelSerializer):
    date_type = serializers.StringRelatedField()

    class Meta:
        model = FindingAidsEntityDate
        exclude = ('id', 'fa_entity')


class FindingAidsEntityCreatorSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    def get_role(self, value):
        if value == 'COL':
            return 'Collector'
        else:
            return 'Creator'

    class Meta:
        model = FindingAidsEntityCreator
        exclude = ('id', 'fa_entity')


class FindingAidsEntityPlaceOfCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindingAidsEntityPlaceOfCreation
        exclude = ('id', 'fa_entity')


class FindingAidsEntitySubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindingAidsEntitySubject
        exclude = ('id', 'fa_entity')


class FindingAidsEntityAssociatedPersonSerializer(serializers.ModelSerializer):
    associated_person = serializers.StringRelatedField()
    role = serializers.StringRelatedField()

    class Meta:
        model = FindingAidsEntityAssociatedPerson
        exclude = ('id', 'fa_entity')


class FindingAidsEntityAssociatedCorporationSerializer(serializers.ModelSerializer):
    associated_corporation = serializers.StringRelatedField()
    role = serializers.StringRelatedField()

    class Meta:
        model = FindingAidsEntityAssociatedCorporation
        exclude = ('id', 'fa_entity')


class FindingAidsEntityAssociatedCountrySerializer(serializers.ModelSerializer):
    associated_country = serializers.StringRelatedField()
    role = serializers.StringRelatedField()

    class Meta:
        model = FindingAidsEntityAssociatedCountry
        exclude = ('id', 'fa_entity')


class FindingAidsEntityAssociatedPlaceSerializer(serializers.ModelSerializer):
    associated_place = serializers.StringRelatedField()
    role = serializers.StringRelatedField()

    class Meta:
        model = FindingAidsEntityAssociatedPlace
        exclude = ('id', 'fa_entity')


class FindingAidsEntityLanguageSerializer(serializers.ModelSerializer):
    language = serializers.StringRelatedField()
    language_usage = serializers.StringRelatedField()

    class Meta:
        model = FindingAidsEntityLanguage
        exclude = ('id', 'fa_entity')


class FindingAidsSerializer(serializers.ModelSerializer):
    archival_unit = ArchivalUnitSerializer()
    level = serializers.SerializerMethodField()
    description_level = serializers.SerializerMethodField()
    primary_type = serializers.StringRelatedField()
    date = FindingAidsEntityDateSerializer(many=True, source='findingaidsentitydate_set')
    genre = serializers.StringRelatedField(many=True)
    spatial_coverage_country = serializers.StringRelatedField(many=True)
    spatial_coverage_place = serializers.StringRelatedField(many=True)
    subject_person = serializers.StringRelatedField(many=True)
    subject_corporation = serializers.StringRelatedField(many=True)
    subject_heading = serializers.StringRelatedField(many=True)
    subject_keyword = serializers.StringRelatedField(many=True)
    alternative_title = FindingAidsAlternativeTitleSerializer(many=True, source='findingaidsentityalternativetitle_set')
    creator = FindingAidsEntityCreatorSerializer(many=True, source='findingaidsentitycreator_set')
    place_of_creation = FindingAidsEntityPlaceOfCreationSerializer(many=True,
                                                                   source='findingaidsentityplaceofcreation_set')
    associated_person = FindingAidsEntityAssociatedPersonSerializer(many=True,
                                                                    source='findingaidsentityassociatedperson_set')
    associated_corporation = FindingAidsEntityAssociatedPersonSerializer(many=True,
                                                                         source='findingaidsentityassociatedcorporation_set')
    associated_country = FindingAidsEntityAssociatedCountrySerializer(many=True,
                                                                      source='findingaidsentityassociatedcountry_set')
    associated_place = FindingAidsEntityAssociatedPlaceSerializer(many=True,
                                                                  source='findingaidsentityassociatedplace_set')
    language = FindingAidsEntityLanguageSerializer(many=True,
                                                   source='findingaidsentitylanguage_set')

    def get_level(self, value):
        if value == 'L1':
            return 'Level 1'
        else:
            return 'Level 2'

    def get_description_level(self, value):
        if value == 'F':
            return 'Folder'
        else:
            return 'Item'

    class Meta:
        model = FindingAidsEntity
        exclude = ('container', )
