from django.conf.urls import url

from api.views import GetSetDigitizedContainer

urlpatterns = [
    url(r'^containers/(?P<barcode>\d+)/$', GetSetDigitizedContainer.as_view(), name='list_set_digitized_container'),
]
