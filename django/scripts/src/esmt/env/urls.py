"""
Author: Yogaraja Gopal
This module takes care of routing the request from env app
"""
from django.conf.urls import url
from . import views, api

app_name = 'env'
urlpatterns = [
    url(r'^all$', views.all_env, name='all'),
    url(r'^r3$', views.r3_env, name='r3'),
    url(r'^r3mod', views.r3_mod, name='r3mod'),
    url(r'^r2', views.r2_env, name='r2'),
    url(r'^plato', views.plato, name='plato'),
    url(r'^socAU', views.soc_aus, name='socAU'),
    url(r'^solar7', views.solar7, name='solar7'),
    url(r'^server/socrates/status/(?P<third_octet>[0-9]+)/$', api.server_status),
    url(r'^service/socrates/(?P<third_octet>[-\w]+)/status/$', api.get_service_status),
    url(r'^storecomms/socrates/(?P<third_octet>[0-9]+)/(?P<action>[a-z]+)/$',
        api.restart_store_comms),
    url(r'^mount/socrates/(?P<r2_r3>[\w]+)/(?P<third_octet>[-\w]+)/$', api.mount_detail_request),
    url(r'^replication/socrates/get/(?P<third_octet>[0-9]+)/(?P<r2_r3>[\w]+)/$',
        api.rundeck_repl_detail_request),
    url(r'^replication/socrates/(?P<third_octet>[0-9]+)/(?P<action>[a-z]+)/$',
        api.process_replication_requests),
    url(r'^eod/socrates/(?P<third_octet>[0-9]+)$', api.process_eod_log_requests),
    url(r'^utils/socrates/(?P<third_octet>[0-9]+)/$', api.utils_detail_request),
    url(r'^facts/socrates/(?P<third_octet>[0-9]+)/(?P<r2_r3>[\w]+)/$', api.fact_detail_request),
    url(r'^service/socrates/(?P<env_region>[-\w]+)/(?P<third_octet>[0-9]+)/(?P<client>[\w]+)/(?P<service_name>[-\w]+)/(?P<action>[a-z]+)/$',
        api.process_service_action),
    url(r'^get_environment/$', api.EnvironmentView.as_view(), name='get_environment'),
    url(r'^environment_add/$', views.EnvironmentAddView.as_view(), name='environment_add'),
    url(r'^map_instance/(?P<env_id>[0-9]+)/(?P<system_id>[0-9]+)/(?P<system_element_id>[0-9]+)/$', views.map_instance, name='map_instance'),
]