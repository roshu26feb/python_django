"""
This module takes care of routing the request from release app
"""
from django.conf.urls import url
from . import views

app_name = 'test_automation'

urlpatterns = [
    url(r'^test_runs/$', views.test_runs, name='test_runs'),
    #url(r'^test_run_create/$', views.CreateTestRunView.as_view(),
    #    name='test_run_create'),
    #url(r'^test_set_create/$', views.CreateTestSetView.as_view(), name='test_set_create'),
]
