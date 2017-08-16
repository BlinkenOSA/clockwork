from django.conf.urls import url

from authority.views.authority_query_views import VIAFTableView, WikipediaTableView, LCSHTableView
from authority.views.country_views import *
from authority.views.corporation_views import *
from authority.views.language_views import *
from authority.views.person_views import *
from authority.views.place_views import *
from authority.views.genre_views import *
from authority.views.subject_views import *

app_name = 'authority'
urlpatterns = [
    url(r'^country/$', CountryList.as_view(), name='country_list'),
    url(r'^country/create/$', CountryCreate.as_view(), name='country_create'),
    url(r'^country/update/(?P<pk>\d+)/$', CountryUpdate.as_view(), name='country_update'),
    url(r'^country/delete/(?P<pk>\d+)/$', CountryDelete.as_view(), name='country_delete'),
    url(r'^country/datatable/$', CountryListJson.as_view(), name='country_list_json'),
    
    url(r'^corporation/$', CorporationList.as_view(), name='corporation_list'),
    url(r'^corporation/create/$', CorporationCreate.as_view(), name='corporation_create'),
    url(r'^corporation/update/(?P<pk>\d+)/$', CorporationUpdate.as_view(), name='corporation_update'),
    url(r'^corporation/delete/(?P<pk>\d+)/$', CorporationDelete.as_view(), name='corporation_delete'),
    url(r'^corporation/datatable/$', CorporationListJson.as_view(), name='corporation_list_json'),
    
    url(r'^person/$', PersonList.as_view(), name='person_list'),
    url(r'^person/create/$', PersonCreate.as_view(), name='person_create'),
    url(r'^person/update/(?P<pk>\d+)/$', PersonUpdate.as_view(), name='person_update'),
    url(r'^person/delete/(?P<pk>\d+)/$', PersonDelete.as_view(), name='person_delete'),
    url(r'^person/datatable/$', PersonListJson.as_view(), name='person_list_json'),
    
    url(r'^language/$', LanguageList.as_view(), name='language_list'),
    url(r'^language/create/$', LanguageCreate.as_view(), name='language_create'),
    url(r'^language/update/(?P<pk>\d+)/$', LanguageUpdate.as_view(), name='language_update'),
    url(r'^language/delete/(?P<pk>\d+)/$', LanguageDelete.as_view(), name='language_delete'),
    url(r'^language/datatable/$', LanguageListJson.as_view(), name='language_list_json'), 
    
    url(r'^place/$', PlaceList.as_view(), name='place_list'),
    url(r'^place/create/$', PlaceCreate.as_view(), name='place_create'),
    url(r'^place/update/(?P<pk>\d+)/$', PlaceUpdate.as_view(), name='place_update'),
    url(r'^place/delete/(?P<pk>\d+)/$', PlaceDelete.as_view(), name='place_delete'),
    url(r'^place/datatable/$', PlaceListJson.as_view(), name='place_list_json'),
    
    url(r'^genre/$', GenreList.as_view(), name='genre_list'),
    url(r'^genre/create/$', GenreCreate.as_view(), name='genre_create'),
    url(r'^genre/update/(?P<pk>\d+)/$', GenreUpdate.as_view(), name='genre_update'),
    url(r'^genre/delete/(?P<pk>\d+)/$', GenreDelete.as_view(), name='genre_delete'),
    url(r'^genre/datatable/$', GenreListJson.as_view(), name='genre_list_json'),     

    url(r'^subject/$', SubjectList.as_view(), name='subject_list'),
    url(r'^subject/create/$', SubjectCreate.as_view(), name='subject_create'),
    url(r'^subject/update/(?P<pk>\d+)/$', SubjectUpdate.as_view(), name='subject_update'),
    url(r'^subject/delete/(?P<pk>\d+)/$', SubjectDelete.as_view(), name='subject_delete'),
    url(r'^subject/datatable/$', SubjectListJson.as_view(), name='subject_list_json'),

    url(r'^viaf_datatable/$', VIAFTableView.as_view(), name='viaf_list_json'),
    url(r'^lcsh_datatable/$', LCSHTableView.as_view(), name='lcsh_list_json'),
    url(r'^wikipedia_datatable/$', WikipediaTableView.as_view(), name='wiki_list_json'),
]
