from django.conf.urls import url

from dashboard import views

urlpatterns = [
    url(r'^statistics/carrier_type/(?P<archival_unit>\d+)/$', views.statistics_carrier_types, name='stat_carrier_type'),
    url(r'^statistics/linear_meter/(?P<archival_unit>\d+)/$', views.statistics_linear_meter, name='stat_linear_meter'),

    url(r'^statistics/published_items/(?P<archival_unit>\d+)/$',
        views.statistics_published_items,
        name='stat_published_items'),

    url(r'^statistics/isad/(?P<archival_unit>\d+)/$', views.statistics_isad, name='stat_isad'),
    url(r'^statistics/duration/(?P<archival_unit>\d+)/$', views.statistics_duration, name='stat_duration'),

    url(r'^infobox/(?P<module>\w+)/(?P<form_element>.*)/$', views.infobox, name='infobox'),
]
