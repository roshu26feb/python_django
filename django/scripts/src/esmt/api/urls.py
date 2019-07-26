"""
Author: Yogaraja Gopal
This module takes care of routing the delivery DB urls
"""
from django.conf.urls import url
from . import api

app_name = 'api'
urlpatterns = [
    url(r'^get/(?P<api_object>[\w_]+)/$', api.PerformApiCall.as_view(), name='get_api_object'),
    url(r'^get_system_by_id/(?P<system_id>[0-9]+)/$', api.SystemByIdView.as_view(),
        name='get_system_by_id'),
    url(r'^get_system_version_by_id/(?P<system_id>[0-9]+)/$', api.SystemVersionByIdView.as_view(),
        name='get_system_version_by_id'),
  
    url(r'^get_system_element_component_by_id/(?P<system_version_id>[0-9]+)/$', api.SystemEleCompByIdView.as_view(),name='get_system_element_component_by_id'),
    url(r'^get_sys_ele_comp_by_sysverid_syseleid/(?P<system_version_id>[0-9]+)/(?P<system_element_id>[0-9]+)/(?P<env_id>[0-9]+)/(?P<instance_id>[0-9]+)/$', api.SystemEleCompBySysVerIdSysEleIdView.as_view(),name='get_sys_ele_comp_by_sysverid_syseleid'),
    url(r'^get_system_element_by_id/(?P<system_id>[0-9]+)/$', api.SystemEleByIdView.as_view(),
        name='get_system_element_by_id'),
    url(r'^get_infra_by_id/(?P<infra_id>[0-9]+)/$', api.InfraById.as_view(),
        name='get_infra_by_id'),
    url(r'^get_release_by_id/(?P<release_id>[0-9]+)/$', api.ReleaseByIdView.as_view(),
        name='get_release_by_id'),
    url(r'^get_parameter/(?P<parameter_id>[0-9]+)/$', api.ParameterByIdAPI.as_view(),
        name='get_parameter_by_id'),
    url(r'^get_linked_item/(?P<link_item>[_\w]+)/$', api.GetLinkedItems.as_view(),
        name='get_linked_item'),
    url(r'^get_instance_from_env/(?P<env_id>[0-9]+)/$', api.InstanceFromEnv.as_view(),
        name='get_instance_from_env'),
    url(r'^get_instance_names/$', api.InstanceName.as_view(), name='get_instance_name'),
    url(r'^get_instance_list/$', api.InstanceList.as_view(), name='get_instance_list'),
    url(r'^get_instance_list_without_destroyed/$', api.InstanceListWithoutDestroyed.as_view(), name='get_instance_list'),
    url(r'^get_infra_template_from_inst/(?P<inst_id>[0-9]+)/$', api.InfraFromInst.as_view(),
        name='get_infra_template_from_inst'),
    url(r'^get_user_by_id/(?P<user_id>[0-9]+)/$', api.UserByIdView.as_view(),
        name='get_user_by_id'),
    url(r'^get_deploy_by_env/(?P<env_id>[0-9]+)/$', api.DeploymentByEnvId.as_view(), name='get_deploy_by_env'),
    url(r'^get_system_element_deploy_version/(?P<inst_id>[0-9]+)/(?P<se_id>[0-9]+)/$', 
        api.SystemElementDeployedVersion.as_view(), name='get_sys_ele_deploy_ver'),
    url(r'^update_deploy_comp_sts/(?P<mode>[\w]+)/(?P<deployment_id>[0-9]+)/(?P<comp_id>[0-9]+)/$',
        api.UpdateDeploymentComponentStatus.as_view(), name='update_deploy_comp_sts'),
    url(r'^call_jenkins_job/(?P<mode>[\w]+)/(?P<deployment_id>[0-9]+)/(?P<comp_id>[0-9]+)/$',
        api.CallJenkinsJob.as_view(), name='call_jenkins_job'),
    url(r'^get_sys_elem_by_env/(?P<env_id>[0-9]+)/$', api.SystemElementByEnvId.as_view(), name='get_sys_elem_by_env'),
    url(r'^get_instance_allocation/(?P<env_id>[0-9]+)/(?P<sys_id>[0-9]+)/(?P<sys_ele_id>[0-9]+)/$', api.InstanceAllocation.as_view(), name='get_instance_allocation'),
    url(r'^get_system_element_by_env_id/(?P<system_id>[0-9]+)/(?P<env_id>[0-9]+)/$', api.SystemElementbyEnvIDView.as_view(),
        name='get_system_element_by_env_id'),
    url(r'^get_sys_ele_comp_by_sysversion_syselem/(?P<system_version_id>[0-9]+)/(?P<system_element_id>[0-9]+)/$', api.SystemComponentbySysversionAndSyselemIDView.as_view(),
        name='get_sys_ele_comp_by_sysversion_syselem'),
    url(r'^get_comp_by_comptype_id/(?P<component_type_id>[0-9]+)/$', api.CompByCompTypeIdView.as_view(),
        name='get_comp_by_comptype_id'),
     url(r'^get_comp_by_comptype_id_FA/(?P<component_type_id>[0-9]+)/$', api.CompByCompTypeIdFAView.as_view(),name='get_comp_by_comptype_id_FA'),

    url(r'^get_sys_ele_comp_by_sysverid_syseleid_env/(?P<system_version_id>[0-9]+)/(?P<system_element_id>[0-9]+)/(?P<env_id>[0-9]+)/(?P<instance_id>[0-9]+)/$', api.SystemEleCompBySysVerIdSysEleIdViewEnv.as_view(),name='get_sys_ele_comp_by_sysverid_syseleid_v2'),
]
