import datetime
from django_date_extensions.fields import ApproximateDate
from rest_framework import serializers

from archival_unit.models import ArchivalUnit
from controlled_list.models import Locale
from finding_aids.models import FindingAidsEntity, FindingAidsEntityAlternativeTitle, FindingAidsEntityDate, \
    FindingAidsEntityCreator, FindingAidsEntityPlaceOfCreation, FindingAidsEntitySubject, \
    FindingAidsEntityAssociatedPerson, FindingAidsEntityAssociatedCorporation, FindingAidsEntityAssociatedCountry, \
    FindingAidsEntityAssociatedPlace, FindingAidsEntityLanguage
from api.serializers.archival_unit_serializer import ArchivalUnitSerializer as ArchivalUnitDetailSerializer


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


class FindingAidsGridSerializer(serializers.ModelSerializer):
    time_start = serializers.DurationField()
    time_end = serializers.DurationField()
    original_locale = serializers.SlugRelatedField(slug_field='locale_name', queryset=Locale.objects.all())

    def to_internal_value(self, data):
        date_from = data.get('date_from', None)
        date_to = data.get('date_to', None)
        time_start = data.get('time_start', None)
        time_end = data.get('time_end', None)
        duration = data.get('duration', None)
        locale = data.get('original_locale', None)
        if time_start:
            hours, minutes, seconds = time_start.split(':')
            data['time_start'] = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        if time_end:
            hours, minutes, seconds = time_end.split(':')
            data['time_end'] = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        if duration:
            hours, minutes, seconds = duration.split(':')
            data['duration'] = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        if date_from:
            data['date_from'] = change_date(date_from, 'date_from')
        if date_to:
            data['date_to'] = change_date(date_to, 'date_to')
        if locale:
            data['original_locale'] = Locale.objects.get(locale_name=locale)
        return data

    class Meta:
        model = FindingAidsEntity
        fields = (
            'id', 'digital_version_exists',
            'archival_reference_code', 'original_locale',
            'title', 'title_original',
            'contents_summary', 'contents_summary_original',
            'date_from', 'date_to', 'time_start', 'time_end', 'duration',
            'note', 'note_original'
        )


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


def change_date(d, field):
    if len(d) == 4:
        return '%s-00-00' % d
    elif len(d) == 7:
        slices = d.split('-')
        if len(slices) != 2:
            raise serializers.ValidationError({field: 'Wrong date format.'})
        else:
            year = int(slices[0])
            month = int(slices[1])
            try:
                ApproximateDate(year=year, month=month, day=0)
                return "%s-00" % d
            except ValueError:
                raise serializers.ValidationError({field: 'Wrong date format.'})
    elif len(d) == 10:
        slices = d.split('-')
        if len(slices) != 3:
            raise serializers.ValidationError({field: 'Wrong date format.'})
        else:
            year = int(slices[0])
            month = int(slices[1])
            day = int(slices[2])
            try:
                ApproximateDate(year=year, month=month, day=day)
                return d
            except ValueError:
                raise serializers.ValidationError({field: 'Wrong date format.'})
    else:
        raise serializers.ValidationError({field: 'Wrong date format.'})


class FADigitizedSerializer(serializers.ModelSerializer):
    archival_unit = ArchivalUnitSerializer(read_only=True)

    class Meta:
        model = FindingAidsEntity
        fields = ['archival_unit', 'title', 'folder_no', 'sequence_no', 'catalog_id', 'archival_reference_code']

