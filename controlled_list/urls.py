from django.conf.urls import url

from controlled_list.views.access_right_view import *
from controlled_list.views.archival_unit_theme_view import *
from controlled_list.views.building_view import *
from controlled_list.views.carrier_type_view import *
from controlled_list.views.corporation_role_view import *
from controlled_list.views.date_type_view import *
from controlled_list.views.extent_unit_view import *
from controlled_list.views.geo_role_view import *
from controlled_list.views.keyword_view import *
from controlled_list.views.language_usage_view import *
from controlled_list.views.person_role_view import *
from controlled_list.views.primary_type_view import *
from controlled_list.views.reproduction_right_view import *
from controlled_list.views.rights_restriction_reason_view import *

urlpatterns = [
    url(r'^access_rights/$', AccessRightList.as_view(), name='access_rights_list'),
    url(r'^access_rights/create/$', AccessRightCreate.as_view(), name='access_rights_create'),
    url(r'^access_rights/update/(?P<pk>\d+)/$', AccessRightUpdate.as_view(), name='access_rights_update'),
    url(r'^access_rights/datatable/$', AccessRightListJson.as_view(), name='access_rights_list_json'),

    url(r'^archival_unit_theme/$', ArchivalUnitThemeList.as_view(), name='archival_unit_theme_list'),
    url(r'^archival_unit_theme/create/$', ArchivalUnitThemeCreate.as_view(), name='archival_unit_theme_create'),
    url(r'^archival_unit_theme/update/(?P<pk>\d+)/$', ArchivalUnitThemeUpdate.as_view(),
        name='archival_unit_theme_update'),
    url(r'^archival_unit_theme/datatable/$', ArchivalUnitThemeListJson.as_view(), name='archival_unit_theme_list_json'),

    url(r'^building/$', BuildingList.as_view(), name='building_list'),
    url(r'^building/create/$', BuildingCreate.as_view(), name='building_create'),
    url(r'^building/update/(?P<pk>\d+)/$', BuildingUpdate.as_view(), name='building_update'),
    url(r'^building/datatable/$', BuildingListJson.as_view(), name='building_list_json'),

    url(r'^carrier_type/$', CarrierTypeList.as_view(), name='carrier_type_list'),
    url(r'^carrier_type/create/$', CarrierTypeCreate.as_view(), name='carrier_type_create'),
    url(r'^carrier_type/update/(?P<pk>\d+)/$', CarrierTypeUpdate.as_view(), name='carrier_type_update'),
    url(r'^carrier_type/datatable/$', CarrierTypeListJson.as_view(), name='carrier_type_list_json'),

    url(r'^corporation_role/$', CorporationRoleList.as_view(), name='corporation_role_list'),
    url(r'^corporation_role/create/$', CorporationRoleCreate.as_view(), name='corporation_role_create'),
    url(r'^corporation_role/update/(?P<pk>\d+)/$', CorporationRoleUpdate.as_view(), name='corporation_role_update'),
    url(r'^corporation_role/datatable/$', CorporationRoleListJson.as_view(), name='corporation_role_list_json'),

    url(r'^date_type/$', DateTypeList.as_view(), name='date_type_list'),
    url(r'^date_type/create/$', DateTypeCreate.as_view(), name='date_type_create'),
    url(r'^date_type/update/(?P<pk>\d+)/$', DateTypeUpdate.as_view(), name='date_type_update'),
    url(r'^date_type/datatable/$', DateTypeListJson.as_view(), name='date_type_list_json'),

    url(r'^extent_unit/$', ExtentUnitList.as_view(), name='extent_unit_list'),
    url(r'^extent_unit/create/$', ExtentUnitCreate.as_view(), name='extent_unit_create'),
    url(r'^extent_unit/update/(?P<pk>\d+)/$', ExtentUnitUpdate.as_view(), name='extent_unit_update'),
    url(r'^extent_unit/datatable/$', ExtentUnitListJson.as_view(), name='extent_unit_list_json'),

    url(r'^geo_role/$', GeoRoleList.as_view(), name='geo_role_list'),
    url(r'^geo_role/create/$', GeoRoleCreate.as_view(), name='geo_role_create'),
    url(r'^geo_role/update/(?P<pk>\d+)/$', GeoRoleUpdate.as_view(), name='geo_role_update'),
    url(r'^geo_role/datatable/$', GeoRoleListJson.as_view(), name='geo_role_list_json'),

    url(r'^keyword/$', KeywordList.as_view(), name='keyword_list'),
    url(r'^keyword/create/$', KeywordCreate.as_view(), name='keyword_create'),
    url(r'^keyword/update/(?P<pk>\d+)/$', KeywordUpdate.as_view(), name='keyword_update'),
    url(r'^keyword/datatable/$', KeywordListJson.as_view(), name='keyword_list_json'),

    url(r'^language_usage/$', LanguageUsageList.as_view(), name='language_usage_list'),
    url(r'^language_usage/create/$', LanguageUsageCreate.as_view(), name='language_usage_create'),
    url(r'^language_usage/update/(?P<pk>\d+)/$', LanguageUsageUpdate.as_view(), name='language_usage_update'),
    url(r'^language_usage/datatable/$', LanguageUsageListJson.as_view(), name='language_usage_list_json'),

    url(r'^person_role/$', PersonRoleList.as_view(), name='person_role_list'),
    url(r'^person_role/create/$', PersonRoleCreate.as_view(), name='person_role_create'),
    url(r'^person_role/update/(?P<pk>\d+)/$', PersonRoleUpdate.as_view(), name='person_role_update'),
    url(r'^person_role/datatable/$', PersonRoleListJson.as_view(), name='person_role_list_json'),

    url(r'^primary_type/$', PrimaryTypeList.as_view(), name='primary_type_list'),
    url(r'^primary_type/create/$', PrimaryTypeCreate.as_view(), name='primary_type_create'),
    url(r'^primary_type/update/(?P<pk>\d+)/$', PrimaryTypeUpdate.as_view(), name='primary_type_update'),
    url(r'^primary_type/datatable/$', PrimaryTypeListJson.as_view(), name='primary_type_list_json'),
    
    url(r'^reproduction_right/$', ReproductionRightList.as_view(), name='reproduction_right_list'),
    url(r'^reproduction_right/create/$', ReproductionRightCreate.as_view(), name='reproduction_right_create'),
    url(r'^reproduction_right/update/(?P<pk>\d+)/$', ReproductionRightUpdate.as_view(),
        name='reproduction_right_update'),
    url(r'^reproduction_right/datatable/$', ReproductionRightListJson.as_view(), name='reproduction_right_list_json'),
    
    url(r'^rights_restriction_reason/$', RightsRestrictionReasonList.as_view(), name='rights_restriction_reason_list'),
    url(r'^rights_restriction_reason/create/$', RightsRestrictionReasonCreate.as_view(),
        name='rights_restriction_reason_create'),
    url(r'^rights_restriction_reason/update/(?P<pk>\d+)/$', RightsRestrictionReasonUpdate.as_view(),
        name='rights_restriction_reason_update'),
    url(r'^rights_restriction_reason/datatable/$', RightsRestrictionReasonListJson.as_view(),
        name='rights_restriction_reason_list_json'),
    
    url(r'^carrier_type/list.json', CarrierTypeJSONList.as_view(), name='carrier_type_json_list'),
    url(r'^primary_type/list.json', PrimaryTypeJSONList.as_view(), name='primary_type_json_list'),
]
