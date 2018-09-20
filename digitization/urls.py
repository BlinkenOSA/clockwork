from django.conf.urls import url

from digitization.views import DigitizationList, DigitizationListJson, DigitizationTechnicalMetadata

urlpatterns = [
    url(r'^$', DigitizationList.as_view(), name='list'),

    url(r'^technical_metadata/(?P<pk>\d+)/$', DigitizationTechnicalMetadata.as_view(), name='technical_metadata'),
    url(r'^datatable/$', DigitizationListJson.as_view(), name='donor_list_json'),
]