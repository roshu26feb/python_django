"""
This module takes care of routing the delivery DB urls
"""
from django.conf.urls import url
from django.views.i18n import javascript_catalog
from . import views


app_name = 'delivery_db'
urlpatterns = [
    url(r'^jsi18n/$', javascript_catalog, name='jsi18n'),
    url(r'^hosts/$', views.host_view, name='hosts'),
    url(r'^instances/$', views.instance_view, name='instances'),
    url(r'^instance_add/$', views.InstanceAddView.as_view(), name='instance_add'),
    url(r'^instance_update/(?P<instance_id>[0-9]+)/$', views.instance_update_view,
        name='instance_update'),
    url(r'^systems/$', views.systems, name='systems'),
    url(r'^system_version_add/$', views.SystemVersionView.as_view(), name='system_version_add'),
    url(r'^system_add/$', views.SystemView.as_view(), name='system_add'),
    url(r'^components/$', views.components, name='components'),
    url(r'^component_version_add/$', views.ComponentVersionView.as_view(),
        name='component_version_add'),
    url(r'^component_add/$', views.ComponentView.as_view(), name='component_add'),
    url(r'^system_component/$', views.system_component, name='system_component'),
    url(r'^infrastructure/$', views.infrastructure, name='infrastructure'),
    url(r'^infra_template_add/$', views.InfraTemplateView.as_view(), name='infra_template_add'),
    url(r'^network_set/$', views.network_set, name='network_set'),
    url(r'^network_set_add/$', views.NetworkSetView.as_view(), name='network_set_add'),
    url(r'^host_type/$', views.host_type, name='host_type'),
    url(r'^host_type_add/$', views.hostTypeView.as_view(), name='host_type_add'),
    url(r'^host_subscription/$', views.host_subscription, name='host_subscription'),
    url(r'^host_subscription_add/$', views.hostSubView.as_view(), name='host_subscription_add'),
    url(r'^host_region/$', views.host_region, name='host_region'),
    url(r'^host_region_add/$', views.hostRegionView.as_view(), name='host_region_add'),
    url(r'^host_site/$', views.host_site, name='host_site'),
    url(r'^host_site_add/$', views.hostSiteView.as_view(), name='host_site_add'),
]
