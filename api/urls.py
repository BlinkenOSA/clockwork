from django.conf.urls import url

from api.views import GetSetDigitizedContainer, GetContainerMetadata

urlpatterns = [
    url(r'^containers/(?P<barcode>\d+)/$', GetSetDigitizedContainer.as_view(), name='list_set_digitized_container'),
    url(r'^containers/metadata/(?P<barcode>\d+)/$', GetContainerMetadata.as_view(), name='list_get_container_metadata'),
]
