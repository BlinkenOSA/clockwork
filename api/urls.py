from django.conf.urls import url

from api.views import GetSetDigitizedContainer, GetContainerMetadata

urlpatterns = [
    url(r'^containers/(?P<barcode>\w+)/$', GetSetDigitizedContainer.as_view(), name='list_set_digitized_container'),
    url(r'^containers/metadata/(?P<barcode>\w+)/$', GetContainerMetadata.as_view(), name='list_get_container_metadata'),
    url(r'^containers/technical_metadata/(?P<barcode>\w+)/$', GetContainerMetadata.as_view(), name='list_get_container_metadata'),
]
