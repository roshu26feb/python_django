"""esmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'', include('esmt.base.urls'), name='base'),
    url(r'^admin/', admin.site.urls),
    url(r'^env/', include('esmt.env.urls'), name='env'),
    url(r'^env_set/', include('esmt.env_set.urls'), name='env_set'),
    url(r'^booking/', include('esmt.booking.urls'), name='booking'),
    url(r'^release/', include('esmt.release.urls'), name='release'),
    url(r'^deployment/', include('esmt.deployment.urls'), name='deployment'),
    url(r'^delivery_db/', include('esmt.delivery_db.urls'), name='delivery_db'),
    url(r'^api/', include('esmt.api.urls'), name='api'),
    url(r'^test_automation/', include('esmt.test_automation.urls'), name='test_automation'),
    url(r'^reporting/', include('esmt.reporting.urls'), name='reporting'),
    url(r'^esmt_admin/', include('esmt.esmt_admin.urls'), name='esmt_admin'),
    url(r'^admin/password_reset/$', auth_views.PasswordResetView.as_view(), name='admin_password_reset',),
    url(r'^admin/password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done', ),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm',),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete',),
]

