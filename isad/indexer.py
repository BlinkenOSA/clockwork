# encoding: utf-8
import json

from django.db.models import Sum, Count
from hashids import Hashids

from container.models import Container
from controlled_list.models import Locale
from isad.models import Isad


class ISADIndexer:
    """
    Class to handle the indexing of an ISAD(G) record.
    """
    def __init__(self, isad_id):
        self.isad = Isad.objects.get(id=isad_id)
        self.hashids = Hashids(salt="osaarchives", min_length=8)
        self.json = {}
        self.solr_document = {}

    def prepare_index(self):
        self._make_solr_document()
        self._make_json()
        if self.isad.original_locale_id:
            self._make_json(locale_id=self.isad.original_locale_id)
        self.solr_document["isad_json"] = json.dumps(self.json)

    def get_solr_id(self):
        return self.hashids.encode(self.isad.archival_unit.fonds * 1000000 +
                                   self.isad.archival_unit.subfonds * 1000 +
                                   self.isad.archival_unit.series)

    def _make_solr_document(self):
        level = self._return_description_level(self.isad.description_level)
        doc = {}
        doc['id'] = self.get_solr_id()
        doc['record_origin'] = 'Archives'
        doc['record_origin_facet'] = 'Archives'
        doc['archival_level'] = 'Archival Unit'
        doc['archival_level_facet'] = 'Archival Unit'

        doc['reference_code'] = self.isad.reference_code
        doc['reference_code_sort'] = self.isad.reference_code
        doc['archival_reference_number_search'] = self.isad.reference_code

        doc['title'] = self.isad.title
        doc['title_e'] = self.isad.title
        doc['title_search'] = self.isad.title
        doc['title_sort'] = self.isad.title

        doc['description_level'] = level
        doc['description_level_facet'] = level

        doc['date_created'] = self._make_date_created_display(self.isad.year_from, self.isad.year_to)
        doc['date_created_search'] = self._make_date_created_search(self.isad.year_from, self.isad.year_to)
        doc['date_created_facet'] = self._make_date_created_search(self.isad.year_from, self.isad.year_to)

        doc['fonds'] = int(self.isad.archival_unit.fonds)
        doc['fonds_sort'] = int(self.isad.archival_unit.fonds)
        doc['subfonds'] = int(self.isad.archival_unit.subfonds)
        doc['subfonds_sort'] = int(self.isad.archival_unit.subfonds)
        doc['series'] = int(self.isad.archival_unit.series)
        doc['series_sort'] = int(self.isad.archival_unit.series)

        if level == "Fonds":
            doc['fonds_name'] = self.isad.archival_unit.get_fonds().title_full
        elif level == "Subfonds":
            doc['subfonds_name'] = self.isad.archival_unit.get_subfonds().title_full

        doc['scope_and_content_narrative_search'] = self.isad.scope_and_content_narrative
        doc['archival_history_search'] = self.isad.archival_history
        doc["publication_note_search"] = self.isad.publication_note

        doc['primary_type'] = "Archival Unit"
        doc['primary_type_facet'] = "Archival Unit"

        languages = " ".join(l.language for l in self.isad.language.all())
        doc['language'] = languages
        doc['language_facet'] = languages

        creators = " ".join(c.creator for c in self.isad.isadcreator_set.all())
        doc['creator'] = creators
        doc['creator_facet'] = creators

        isaar_creators = " ".join(i.name for i in self.isad.isaar.all())
        doc['creator'] = isaar_creators
        doc['creator_facet'] = isaar_creators

        themes = " ".join(t.theme for t in self.isad.archival_unit.theme.all())
        doc['archival_unit_theme'] = themes
        doc['archival_unit_theme_facet'] = themes

        if self.isad.original_locale_id:
            locale = self.isad.original_locale_id.lower()

            if self.isad.archival_unit.title_original:
                doc['title_search_%s' % locale] = self.isad.archival_unit.title_original
                doc['title_original'] = self.isad.archival_unit.title_original
                doc['title_original_e'] = self.isad.archival_unit.title_original

            if self.isad.scope_and_content_narrative_original:
                doc['scope_and_content_narrative_search_hu'] = self.isad.scope_and_content_narrative_original

            if self.isad.archival_history_original:
                doc['archival_history_search_%s' % locale] = self.isad.archival_history_original

            if self.isad.publication_note_original:
                doc['publication_note_search_%s' % locale] = self.isad.publication_note_original

        self.solr_document = doc

    def _make_json(self, locale_id='en'):
        locale = locale_id.lower()

        j = {}

        j['id'] = self.solr_document['id']
        j['referencde_code'] = self.isad.reference_code
        j["descriptionLevel"] = self.solr_document['description_level']

        j["dateFrom"] = self.isad.year_from
        j["dateTo"] = self.isad.year_to
        j["datePredominant"] = self.isad.date_predominant

        j["accruals"] = self.isad.accruals
        j["referenceCode"] = self.isad.reference_code

        j["languages"] = [l.language for l in self.isad.language.all()]

        if self.isad.access_rights:
            j["rightsAccess"] = self.isad.access_rights.statement

        if self.isad.access_rights_legacy:
            j["rightsAccess"] = self.isad.access_rights_legacy

        if self.isad.reproduction_rights:
            j["rightsReproduction"] = self.isad.reproduction_rights.statement

        if self.isad.reproduction_rights_legacy:
            j["rightsReproduction"] = self.isad.reproduction_rights_legacy

        creator = []
        for c in self.isad.isadcreator_set.all():
            creator.append(c.creator)

        for c in self.isad.isaar.all():
            creator.append(c.name)
        j["creator"] = creator

        related_finding_aids = []
        for rfa in self.isad.isadrelatedfindingaids_set.all():
            related_finding_aids.append({'info': rfa.info, 'url': rfa.url})
        j["relatedUnits"] = related_finding_aids

        j["rightsReproduction"] = self.isad.reproduction_rights_legacy

        if locale == 'en':
            j["title"] = self.isad.title
            j["archivalHistory"] = self.isad.archival_history
            j["scopeAndContentNarrative"] = self.isad.scope_and_content_narrative.replace('\n', '<br />') \
                if self.isad.scope_and_content_narrative else None
            j["scopeAndContentAbstract"] = self.isad.scope_and_content_abstract.replace('\n', '<br />') \
                if self.isad.scope_and_content_abstract else None
            j["appraisal"] = self.isad.appraisal
            j["physicalCharacteristics"] = self.isad.physical_characteristics
            j["publicationNote"] = self.isad.publication_note
            j["note"] = self.isad.note
            j["archivistsNote"] = self.isad.archivists_note
            j["extent_estimated"] = self.isad.carrier_estimated
            j["extent"] = self._return_extent()
            j = dict((k, v) for k, v in j.iteritems() if v)
            self.json['isad_json_eng'] = json.dumps(j)
        else:
            j["metadataLanguage"] = Locale.objects.get(pk=locale_id).locale_name
            j["metadataLanguageCode"] = locale
            j["title"] = self.isad.archival_unit.title_original
            j["archivalHistory"] = self.isad.archival_history_original
            j["scopeAndContentNarrative"] = self.isad.scope_and_content_narrative_original.replace('\n', '<br />') \
                if self.isad.scope_and_content_narrative_original else None
            j["scopeAndContentAbstract"] = self.isad.scope_and_content_abstract_original.replace('\n', '<br />') \
                if self.isad.scope_and_content_abstract_original else None
            j["appraisal"] = self.isad.appraisal_original
            j["physicalCharacteristics"] = self.isad.physical_characteristics_original
            j["publicationNote"] = self.isad.publication_note_original
            j["note"] = self.isad.note_original
            j["archivistsNote"] = self.isad.archivists_note_original
            j["extent_estimated"] = self.isad.carrier_estimated_original if locale_id == 'HU' else self.isad.carrier_estimated
            j["extent"] = self._return_extent(lang=locale_id.lower())

            if self.isad.access_rights_legacy:
                j["rightsAccess"] = self.isad.access_rights_legacy_original

            j = dict((k, v) for k, v in j.iteritems() if v)
            self.json['isad_json_2nd'] = json.dumps(j)

    def _make_date_created_search(self, year_from, year_to):
        date = []

        if year_to:
            for year in xrange(year_from, year_to + 1):
                date.append(year)
        else:
            date.append(str(year_from))

        return date

    def _make_date_created_display(self, year_from, year_to):
        if year_from > 0:
            date = str(year_from)

            if year_to:
                if year_from!= year_to:
                    date = date + " - " + str(year_to)
        else:
            date = ""

        return date

    def _return_description_level(self, description_level):
        levels = {
            'F': 'Fonds',
            'SF': 'Subfonds',
            'S': 'Series'
        }
        return levels[description_level]

    def _return_extent(self, lang='en'):
        extent = []
        total = 0

        archival_unit = self.isad.archival_unit

        if archival_unit.level == 'F':
            containers = Container.objects.filter(archival_unit__fonds=archival_unit.fonds)
        elif archival_unit.level == 'SF':
            containers = Container.objects.filter(archival_unit__fonds=archival_unit.fonds,
                                                  archival_unit__subfonds=archival_unit.subfonds)
        else:
            containers = Container.objects.filter(archival_unit=archival_unit)

        containers = containers.values('carrier_type__type', 'carrier_type__type_original_language')\
            .annotate(width=Sum('carrier_type__width'), number=Count('id'))

        for c in containers:
            if lang == 'hu':
                extent.append(str(c['number']) + ' ' + c['carrier_type__type_original_language'] + ', ' +
                              str(round(c['width']/1000.00, 2)) + u' folyóméter')
            elif lang == 'pl':
                extent.append(str(c['number']) + ' ' + c['carrier_type__type'] + ', ' +
                              str(round(c['width']/1000.00, 2)) + u' metr bieżący')
            elif lang == 'it':
                extent.append(str(c['number']) + ' ' + c['carrier_type__type'] + ', ' +
                              str(round(c['width']/1000.00, 2)) + u' metro lineare')
            else:
                extent.append(str(c['number']) + ' ' + c['carrier_type__type'] + ', ' +
                              str(round(c['width']/1000.00, 2)) + ' linear meters')

        return extent
