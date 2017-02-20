from django.conf.urls import url

from donor.views import DonorList, DonorDetail, DonorCreate, DonorUpdate, DonorDelete, DonorListJson, DonorPopupCreate

urlpatterns = [
    url(r'^$', DonorList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', DonorDetail.as_view(), name='view'),
    url(r'^create/$', DonorCreate.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', DonorUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', DonorDelete.as_view(), name='delete'),

    url(r'^popup/create/$', DonorPopupCreate.as_view(), name='create_popup'),

    url(r'^datatable/$', DonorListJson.as_view(), name='donor_list_json'),
]
