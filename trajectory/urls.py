from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'trajectory.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','showpath.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^measurement/(?P<id>\d+)/$', 'showpath.views.measurement'),
    url(r'^roadseg/(?P<id>\d+)/$','showpath.views.roadseg'),
    url(r'^pointgroup/(?P<id>[0-9\+]+)/$','showpath.views.pointgroup'),
    url(r'^linegroup/(?P<id>[0-9\+]+)/$','showpath.views.linegroup'),
    url(r'^test/(?P<time>\d+)/$','showpath.views.testlist'),
    url(r'^test/(?P<time>\d+)/(?P<id>\d+)/$', 'showpath.views.test'),
    url(r'^truepath/measurement/(?P<id>\d+)/$', 'truepath.views.measurements'),
    url(r'^truepath/segments/(?P<id>\d+)/$','truepath.views.segments'),
    url(r'^truepath/mm_segments/(?P<id>\d+)/$','truepath.views.mm_segments'),
    url(r'^truepath/projected/(?P<id>\d+)/$','truepath.views.projected_points'),
    url(r'^truepath/$','truepath.views.testlist',name='testlist'),
    url(r'^truepath/(?P<id>[0-9\+]+)/$','truepath.views.test', name="test"),
    url(r'^truepath/edges/(?P<id>[0-9\+]+)/$','truepath.views.edges'),
    url(r'^truepath/update/$','truepath.views.update'),
]
