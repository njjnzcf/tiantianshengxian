from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^index$', views.index,name='index'),
    url(r'^list_(\d+)_(\d+)_(\d+)$', views.list, name='list'),
    url(r'^(\d+)$', views.detail, name='detail'),
]