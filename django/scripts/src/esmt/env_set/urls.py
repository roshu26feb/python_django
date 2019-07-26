"""
Author: Yogaraja Gopal
Comment: This module handles URLs for Env_Set App
"""
from django.conf.urls import url
from . import views, api

app_name = 'env_set'

urlpatterns = [
    url(r'^all$', views.all_env_set, name='all'),
    url(r'^env_set_add/$', views.EnvironmentSetAddView.as_view(), name='env_set_add'),
    url(r'^sit', views.sit, name='sit'),
    url(r'^two', views.two, name='two'),
    url(r'^uat', views.uat, name='uat'),
    url(r'^pre_prod', views.pre_prod, name='pre_prod'),
    url(r'^data/(?P<file_name>[-\w]+)/$', api.get_server_data_file),
    url(r'^static/data/ping/$', api.get_ping_data),
    url(r'^service/socrates/(?P<env_region>[-\w]+)/(?P<service_name>[-\w]+)/(?P<action>[a-z]+)/'
        r'(?P<client>[\w]+)/$', api.process_soc_requests),
    url(r'^service/plato/(?P<plato_region>[\w]+)/(?P<service_name>[\w]+)/(?P<action>[a-z]+)/',
        api.process_plato_requests),
    url(r'^service/aristotle/(?P<service_name>[-\w]+)/(?P<action>[a-z]+)/(?P<third_octet>[0-9]+)/$',
        api.process_aristo_requests),
    url(r'^service/solar7/(?P<solar7_region>[-\w]+)/(?P<service_name>[\w]+)/(?P<action>[a-z]+)/$',
        api.process_solar7_requests),
    url(r'^status/interface/$', api.get_interface_status),
]
