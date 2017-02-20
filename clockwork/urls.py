from django.conf.urls import include, url

from django.contrib.auth import views as auth_views
from dashboard import views as dashboard_view

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, name='logout'),

    url(r'^$', dashboard_view.index, name='dashboard'),
    url(r'^controlled_list/', include('controlled_list.urls', namespace='controlled_list')),
    url(r'^archival_unit/', include('archival_unit.urls', namespace='archival_unit')),
    url(r'^accession/', include('accession.urls', namespace='accession')),
    url(r'^authority/', include('authority.urls', namespace='authority')),
    url(r'^donor/', include('donor.urls', namespace='donor')),
    url(r'^isaar/', include('isaar.urls', namespace='isaar')),
    url(r'^isad/', include('isad.urls', namespace='isad')),
    url(r'^container/', include('container.urls', namespace='container')),
    url(r'^finding_aids/', include('finding_aids.urls', namespace='finding_aids')),


    url(r'^select2/', include('django_select2.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
]
