from django.conf.urls import url
from . import views

app_name = 'booking'

urlpatterns = [
    url(r'^r3/$', views.r3, name='r3'),
    url(r'^r2/$', views.r2, name='r2'),
    url(r'^plato/$', views.plato, name='plato'),
    url(r'^och/$', views.och, name='och')
]
