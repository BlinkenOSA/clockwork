import json

import requests
from braces.views import JSONResponseMixin
from django.views.generic import View


class VIAFMixin(object):
    def get_results_from_viaf(self, query, request_type):
        if len(query) == 0 or len(request_type) == 0:
            return {}
        else:
            if request_type == 'person':
                query = 'local.personalNames+all+"' + query + '"'

            session = requests.Session()
            session.trust_env = False

            r = session.get('http://www.viaf.org/viaf/search?query=%s&sortKeys=holdingscount&maximumRecords=5&httpAccept'
                            '=application/json&recordSchema=http://viaf.org/BriefVIAFCluster' % query)
            if r.status_code == 200:
                return self.assemble_data_stream(json.loads(r.text))
            else:
                return {}

    def assemble_data_stream(self, json_data):
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
                    'viaf_id': viaf_id,
                    'name': name,
                    'action': '<button class="btn btn-default btn-xs select-viaf">Select</button>'
                }
                data.append(rec)
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


class WikipediaTableView(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = []
        context = {
            "draw": request.GET['draw'],
            "data": data,
            "recordsFiltered": 0,
            "recordsTotal": 0,
            "result": "ok"
        }
        return self.render_json_response(context)
