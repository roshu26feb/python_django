"""
This module takes care of routing the request from release app
"""
from django.conf.urls import url
from . import views

app_name = 'release'

urlpatterns = [
    url(r'^releases/$', views.releases, name='releases'),
    url(r'^release_version_add/$', views.ReleaseVersionAddView.as_view(),
        name='release_version_add'),
    url(r'^release_add/$', views.ReleaseAddView.as_view(), name='release_add'),
    url(r'^rtl/$', views.RouteToLiveView.as_view(), name='rtl'),
    url(r'^manage_rtl/$', views.manage_rtl, name='manage_rtl'),
]
