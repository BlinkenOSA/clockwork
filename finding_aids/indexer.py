# encoding: utf-8
import json
from base64 import b64encode

from hashids import Hashids

from controlled_list.models import Locale
from finding_aids.models import FindingAidsEntity


class FindingAidsEntityIndexer:
    """
    Class to handle the indexing of a Finding Aids record.
    """
    def __init__(self, finding_aids_entity_id):
        self.finding_aids = FindingAidsEntity.objects.get(id=finding_aids_entity_id)

        self.original_locale = ""
        self.json = {}
        self.solr_document = {}

    def prepare_index(self):
        self._get_original_locale()
        self._make_solr_document()
        self._make_json()
        if self.original_locale != "":
            self._make_json(lang=self.original_locale)
        self.solr_document["item_json"] = json.dumps(self.json)
        self.solr_document["item_json_e"] = b64encode(json.dumps(self.json))

    def prepare_confidential_index(self):
        self._make_solr_confidential_document()
        self._make_confidential_json()
        self.solr_document["item_json"] = json.dumps(self.json)
        self.solr_document["item_json_e"] = b64encode(json.dumps(self.json))

    def get_solr_id(self):
        if self.finding_aids.catalog_id:
            return self.finding_aids.catalog_id
        else:
            hashids = Hashids(salt="osacontent", min_length=10)
            return hashids.encode(self.finding_aids.id)

    def _get_original_locale(self):
        if self.finding_aids.original_locale:
            self.original_locale = self.finding_aids.original_locale.id.lower()

    def _make_solr_document(self):
        doc = {}
        doc["id"] = self.get_solr_id(),
        doc["record_origin"] = "Archives",
        doc["record_origin_facet"] = "Archives",
        doc["call_number"] = self.finding_aids.archival_reference_code

        doc["archival_level"] = "Folder/Item",
        doc["archival_level_facet"] = "Folder/Item",

        doc["description_level"] = "Folder" if self.finding_aids.level == 'F' else 'Item'
        doc["description_level_facet"] = "Folder" if self.finding_aids.level == 'F' else 'Item'

        doc["title"] = self.finding_aids.title
        doc["title_e"] = self.finding_aids.title
        doc["title_search"] = self.finding_aids.title
        doc["title_sort"] = self.finding_aids.title

        doc["fonds_sort"] = self.finding_aids.archival_unit.fonds
        doc["subfonds_sort"] = self.finding_aids.archival_unit.subfonds
        doc["series_sort"] = self.finding_aids.archival_unit.series

        doc["container_type"] = self.finding_aids.container.carrier_type.type
        doc["container_type_esort"] = self.finding_aids.container.carrier_type.id

        doc["container_number"] = self.finding_aids.container.container_no
        doc["container_number_sort"] = self.finding_aids.container.container_no

        if self.finding_aids.description_level == 'L1':
            doc["sequence_number"] = self.finding_aids.folder_no
            doc["sequence_number_sort"] = self.finding_aids.folder_no
        else:
            doc["sequence_number"] = self.finding_aids.sequence_no
            doc["sequence_number_sort"] = self.finding_aids.sequence_no

        doc["series_id"] = self._get_series_id()
        doc["series_name"] = self.finding_aids.archival_unit.title_full
        doc["series_reference_code"] = self.finding_aids.archival_unit.reference_code.replace('HU OSA', '')

        doc["contents_summary_search"] = self.finding_aids.contents_summary

        doc["primary_type"] = self.finding_aids.primary_type.type
        doc["primary_type_facet"] = self.finding_aids.primary_type.type

        date_created_display = self._make_date_created_display()
        if date_created_display != "":
            doc["date_created"] = date_created_display

        date_created_search = self._make_date_created_search()
        if date_created_search:
            doc["date_created_facet"] = date_created_search
            doc["date_created_search"] = date_created_search

        doc["duration"] = self._calculate_duration(self.finding_aids.duration)

        genres = [genre.genre for genre in self.finding_aids.genre.all()]
        doc["genre_facet"] = genres

        languages = [language.language for language in self.finding_aids.findingaidsentitylanguage_set.all()]
        doc["language_facet"] = languages

        associated_countries = [ac.associated_country for ac in
                                self.finding_aids.findingaidsentityassociatedcountry_set.all()]
        doc["associated_country_search"] = associated_countries
        doc["added_geo_facet"] = associated_countries

        # Creators
        locale = self.original_locale

        doc["title_original"] = self.finding_aids.title_original
        doc["title_search_%s" % locale] = self.finding_aids.title_original

        self.solr_document = doc

    def _make_json(self, lang='en'):
        j = {}
        if lang == 'en':
            j['id'] = self.get_solr_id()
            j['title'] = self.finding_aids.title
            j['titleOriginal'] = self.finding_aids.title_original
            j['level'] = "Folder" if self.finding_aids.level == 'F' else 'Item'
            j['primaryType'] = self.finding_aids.primary_type.type
            j["containerNumber"] = self.finding_aids.container.container_no
            j["containerType"] = self.finding_aids.container.carrier_type.type

            j["seriesReferenceCode"] = self.finding_aids.archival_unit.reference_code.replace('HU OSA ', '')

            if self.finding_aids.description_level == 'L1':
                j["sequenceNumber"] = self.finding_aids.folder_no
            else:
                j["sequenceNumber"] = self.finding_aids.sequence_no

            j["form_genre"] = [genre.genre for genre in self.finding_aids.genre.all()]
            j["note"] = self.finding_aids.note

            j["contentsSummary"] = self.finding_aids.contents_summary

            j["language"] = [language.language for language in self.finding_aids.findingaidsentitylanguage_set.all()]
            j["languageStatement"] = self.finding_aids.language_statement

            time_start = self.finding_aids.time_start
            if time_start:
                ts_sec = time_start.total_seconds()
                ts_hours = ts_sec // 3600
                ts_minutes = (ts_sec % 3600) // 60
                ts_seconds = ts_sec % 60
                j["timeStart"] = "%02d:%02d:%02d" % (ts_hours, ts_minutes, ts_seconds)

            time_end = self.finding_aids.time_end
            if time_end:
                te_sec = time_end.total_seconds()
                te_hours = te_sec // 3600
                te_minutes = (te_sec % 3600) // 60
                te_seconds = te_sec % 60
                j["timeEnd"] = "%02d:%02d:%02d" % (te_hours, te_minutes, te_seconds)

            duration = self._calculate_duration(self.finding_aids.duration)
            j["duration"] = duration

            contributors = []
            for contributor in self.finding_aids.findingaidsentityassociatedperson_set.all():
                contributors.append({'name': contributor.associated_person, 'role': contributor.role})
            for contributor in self.finding_aids.findingaidsentityassociatedcorporation_set.all():
                contributors.append({'name': contributor.associated_corporation, 'role': contributor.role})
            j["contributors"] = contributors

            j["associatedCountry"] = [country.country for
                                      country in self.finding_aids.findingaidsentityassociatedcountry_set.all()]

            j["dateCreated"] = self._make_date_created_display()

            j["dates"] = []
            for date in self.finding_aids.findingaidsentitydate_set.all():
                j["dates"].append(
                    {"dateType": date.date_type.type, "date": self._make_date_display(date)}
                )

            # Remove empty json keys
            j = dict((k, v) for k, v in j.iteritems() if v)

            self.json['item_json_eng'] = j
        else:
            j = {}
            j["metadataLanguage"] = Locale.objects.get(pk=lang.upper()).locale_name
            j["contentsSummary"] = self.finding_aids.contents_summary_original

            # Remove empty json keys
            j = dict((k, v) for k, v in j.iteritems() if v)

            self.json['item_json_2nd'] = j

    def _make_solr_confidential_document(self):
        doc = {}
        doc["id"] = self.get_solr_id(),
        doc["record_origin"] = "Archives",
        doc["record_origin_facet"] = "Archives",
        doc["call_number"] = self.finding_aids.archival_reference_code

        doc["archival_level"] = "Folder/Item",
        doc["archival_level_facet"] = "Folder/Item",

        doc["description_level"] = "Folder" if self.finding_aids.level == 'F' else 'Item'
        doc["description_level_facet"] = "Folder" if self.finding_aids.level == 'F' else 'Item'

        doc["fonds_sort"] = self.finding_aids.archival_unit.fonds
        doc["subfonds_sort"] = self.finding_aids.archival_unit.subfonds
        doc["series_sort"] = self.finding_aids.archival_unit.series

        doc["container_type"] = self.finding_aids.container.carrier_type.type
        doc["container_type_esort"] = self.finding_aids.container.carrier_type.id

        doc["container_number"] = self.finding_aids.container.container_no
        doc["container_number_sort"] = self.finding_aids.container.container_no

        if self.finding_aids.description_level == 'L1':
            doc["sequence_number"] = self.finding_aids.folder_no
            doc["sequence_number_sort"] = self.finding_aids.folder_no
        else:
            doc["sequence_number"] = self.finding_aids.sequence_no
            doc["sequence_number_sort"] = self.finding_aids.sequence_no

        doc["series_id"] = self._get_series_id()
        doc["series_name"] = self.finding_aids.archival_unit.title_full
        doc["series_reference_code"] = self.finding_aids.archival_unit.reference_code.replace('HU OSA', '')

        if self.finding_aids.confidential_display_text:
            doc["title"] = self.finding_aids.confidential_display_text
        else:
            doc["title"] = "The document is not published because of confidentiality reason."
        self.solr_document = doc

    def _make_confidential_json(self):
        j = {}

        if self.finding_aids.confidential_display_text:
            j["title"] = self.finding_aids.confidential_display_text
        else:
            j["title"] = "The document is not published because of confidentiality reason."
        self.json['item_json_eng'] = j

        j['id'] = self.get_solr_id()
        j['level'] = "Folder" if self.finding_aids.level == 'F' else 'Item'
        j['primaryType'] = self.finding_aids.primary_type.type
        j["containerNumber"] = self.finding_aids.container.container_no
        j["containerType"] = self.finding_aids.container.carrier_type.type

        j["seriesReferenceCode"] = self.finding_aids.archival_unit.reference_code.replace('HU OSA ', '')

        if self.finding_aids.description_level == 'L1':
            j["sequenceNumber"] = self.finding_aids.folder_no
        else:
            j["sequenceNumber"] = self.finding_aids.sequence_no
        self.json['item_json_eng'] = j

    def _get_series_id(self):
        hashids = Hashids(salt="osaarchives", min_length=8)
        return hashids.encode(self.finding_aids.archival_unit.fonds * 1000000 +
                              self.finding_aids.archival_unit.subfonds * 1000 +
                              self.finding_aids.archival_unit.series)

    def _make_date_display(self, date_object):
        date_from = date_object.date_from
        date_to = date_object.date_to

        return "%s - %s" % (date_from, date_to)

    def _make_date_created_display(self):
        if len(self.finding_aids.date_from) == 4:
            year_from = self.finding_aids.date_from
        else:
            year_from = self.finding_aids.date_from.year

        if self.finding_aids.date_to:
            if len(self.finding_aids.date_to) == 4:
                year_from = self.finding_aids.date_to
            else:
                year_to = self.finding_aids.date_to.year
        else:
            year_to = None

        if year_from > 0:
            date = str(year_from)

            if year_to:
                if year_from!= year_to:
                    date = date + " - " + str(year_to)
        else:
            date = ""

        return date

    def _make_date_created_search(self):
        date = []
        year_from = self.finding_aids.date_from.year
        if self.finding_aids.date_to:
            year_to = self.finding_aids.date_to.year
        else:
            year_to = None

        if year_from > 0:
            if year_to:
                for year in xrange(year_from, year_to + 1):
                    date.append(year)
            else:
                date.append(str(year_from))

        return date

    def _calculate_duration(self, duration):
        duration_string = []
        if duration:
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours == 1:
                duration_string.append("%s hour" % hours)

            if hours > 1:
                duration_string.append("%s hours" % hours)

            if minutes > 0:
                duration_string.append("%s min." % minutes)
            if seconds > 0:
                duration_string.append("%s sec." % seconds)
        return ' '.join(duration_string)
