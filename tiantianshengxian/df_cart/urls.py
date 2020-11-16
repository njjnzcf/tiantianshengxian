from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^cart$', views.cart, name='cart'),
]