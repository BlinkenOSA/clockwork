from django.conf.urls import include, url

import dashboard

urlpatterns = [
    url(r'^infobox/(?P<module>\w+)/(?P<form_element>.*)/$', dashboard.views.infobox, name='infobox'),
]