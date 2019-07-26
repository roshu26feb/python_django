"""
This module takes care of routing the request from release app
"""
from django.conf.urls import url
from . import views

app_name = 'deployment'

urlpatterns = [
    url(r'^deployment/$', views.deployment, name='deployment'),
    url(r'^deployment_request/(?P<system_element_id>[0-9]+)/(?P<system_version_id>[0-9]+)/$', views.deployment_request_view,
        name='deployment_request'),
    #url(r'^deployment_add/$', views.CreateDeploymentView.as_view(), name='deployment_add'),
    url(r'^yamlgeneration/$', views.yamlgeneration, name='yamlgeneration'),

 
]
