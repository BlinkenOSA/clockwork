from django.conf.urls import url

from controlled_list.views import CarrierTypeJSONList, PrimaryTypeJSONList, BuildingList, BuildingListJson

urlpatterns = [
    url(r'^building/$', BuildingList.as_view(), name='building_list'),

    url(r'^carrier_type/list.json', CarrierTypeJSONList.as_view(), name='carrier_type_json_list'),
    url(r'^primary_type/list.json', PrimaryTypeJSONList.as_view(), name='primary_type_json_list'),

    url(r'^building/datatable/$', BuildingListJson.as_view(), name='building_list_json'),

]
