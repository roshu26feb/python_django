"""
Author: Yogaraja Gopal
Date : 12-04-2018
This module contains the Urls used for Esmt Admin
"""
from django.conf.urls import url
from . import views

app_name = 'esmt_admin'

urlpatterns = [
    url(r'^user_roles/$', views.user_roles, name='user_roles'),
    url(r'^ref_data_manager/$', views.ref_data_manager, name='ref_data_manager'),
    url(r'^deploy_parameter/$', views.deploy_parameter, name='deploy_parameter'),
    url(r'^parameter_add/$', views.parameter_add_update, name='parameter_add'),
    url(r'^parameter_update/(?P<parameter_id>[0-9]+)/$', views.parameter_add_update,
        name='parameter_update'),
    url(r'^reference_data/$', views.ReferenceDataView.as_view(), name='reference_data'),
    url(r'^add_user/$', views.AddUserView.as_view(), name='add_user'),
    url(r'^user_role_add/$', views.UserRoleAddView.as_view(), name='user_role_add'),
    url(r'^view_user/$', views.view_user, name='view_user')
]
