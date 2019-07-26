"""
Author: Yogaraja Gopal
This module is used to handle URLs for esmt_base app
"""
from django.conf.urls import url, include
from django.contrib.auth import views as auth_view
from . import views

app_name = 'base'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
