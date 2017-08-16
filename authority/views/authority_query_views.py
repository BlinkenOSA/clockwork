import json

import requests
import wikipedia
from braces.views import JSONResponseMixin
from django.views.generic import View


class VIAFMixin(object):
    def get_results_from_viaf(self, query, request_type):
        if len(query) == 0 or len(request_type) == 0:
            return {}
        else:
            if request_type == 'person':
                query = 'local.personalNames+all+"' + query + '"'
            elif request_type == 'corporation':
                query = 'local.corporateNames+all+"' + query + '"'
            elif request_type == 'country':
                query = 'local.geographicNames+all+"' + query + '"'
            elif request_type == 'place':
                query = 'local.geographicNames+all+"' + query + '"'

            session = requests.Session()
            session.trust_env = False

            r = session.get('http://www.viaf.org/viaf/search?query=%s&sortKeys=holdingscount&maximumRecords=5&httpAccept'
                            '=application/json&recordSchema=http://viaf.org/BriefVIAFCluster' % query)
            if r.status_code == 200:
                return self.assemble_data_stream(json.loads(r.text))
            else:
                return {}


    @staticmethod
    def assemble_data_stream(json_data):
        data = []
        counter = 1
        if 'records' in json_data['searchRetrieveResponse']:
            for record in json_data['searchRetrieveResponse']['records']:
                record_data = record['record']['recordData']
                viaf_id = 'http://www.viaf.org/viaf/%s' % record_data['viafID']['#text']

                if isinstance(record_data['v:mainHeadings']['data'], list):
                    name = record_data['v:mainHeadings']['data'][0]['text']
                else:
                    name = record_data['v:mainHeadings']['data']['text']

                rec = {
                    'DT_RowId': counter,
                    'viaf_id': '<a href="%s" target="_blank">%s</a>' % (viaf_id, viaf_id),
                    'name': name,
                    'action': '<a href="#" class="btn btn-default btn-xs select_viaf">Select</a>'
                }
                data.append(rec)
                counter += 1
        return data


class WikipediaMixin(object):
    def get_wikilinks(self, query):
        data = []
        counter = 0
        languages = ['en', 'ru', 'hu', 'de', 'pl', 'it', 'es', 'fr', 'ro', 'cs', 'bg', 'uk']

        for lang in languages:
            wikipedia.set_lang(lang)

            if len(query) > 0:
                ws = wikipedia.search(query, results=2)
                for entry in ws:
                    wiki_url = 'http://%s.wikipedia.org/wiki/%s' % (lang, entry)
                    d = {
                        'DT_RowId': counter,
                        'wiki_url': '<a href="%s" target="_blank">%s</a>' % (wiki_url, wiki_url),
                        'name': entry,
                        'action': '<a href="#" class="btn btn-default btn-xs select_wiki">Select</a>'
                    }
                    counter += 1
                    data.append(d)

        return data


class LCSHMixin(object):
    def get_lcshlinks(self, query, request_type):
        if request_type == 'genre':
            rt = 'http://id.loc.gov/authorities/genreForms'
        elif request_type == 'subject':
            rt = 'http://id.loc.gov/authorities/subjects'

        if len(query) == 0 or len(request_type) == 0:
            return {}
        else:
            session = requests.Session()
            session.trust_env = False

            r = session.get('http://id.loc.gov/search/?q=%s&q=cs:%s&format=json'
                            % (query, rt))
            if r.status_code == 200:
                return self.assemble_data_stream(json.loads(r.text))
            else:
                return {}

    @staticmethod
    def assemble_data_stream(json_data):
        data = []
        counter = 1

        for record in json_data:
            if isinstance(record, list):
                if record[0] == 'atom:entry':
                    lcsh_id = record[3][1]['href']
                    rec = {
                        'DT_RowId': counter,
                        'lcsh_id': '<a href="%s" target="_blank">%s</a>' % (lcsh_id, lcsh_id),
                        'name': record[2][2],
                        'action': '<a href="#" class="btn btn-default btn-xs select_lcsh">Select</a>'
                    }
                    data.append(rec)
                    counter += 1
        return data


class VIAFTableView(VIAFMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):

        query = request.GET['q'] if 'q' in request.GET else ""
        request_type = request.GET['auth_type'] if 'auth_type' in request.GET else ""
        data = self.get_results_from_viaf(query.strip(), request_type.strip())

        context = {
            "draw": request.GET['draw'],
            "data": data,
            "recordsFiltered": 1,
            "recordsTotal": len(data),
            "result": "ok"
        }
        return self.render_json_response(context)


class WikipediaTableView(WikipediaMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):

        query = request.GET['q'] if 'q' in request.GET else ""
        data = self.get_wikilinks(query)

        context = {
            "draw": request.GET['draw'],
            "data": data,
            "recordsFiltered": 0,
            "recordsTotal": len(data),
            "result": "ok"
        }
        return self.render_json_response(context)


class LCSHTableView(LCSHMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):

        query = request.GET['q'] if 'q' in request.GET else ""
        request_type = request.GET['auth_type'] if 'auth_type' in request.GET else ""
        data = self.get_lcshlinks(query.strip(), request_type.strip())

        context = {
            "draw": request.GET['draw'],
            "data": data,
            "recordsFiltered": 0,
            "recordsTotal": len(data),
            "result": "ok"
        }
        return self.render_json_response(context)