#coding=utf-8
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^cart$', views.cart, name='cart'),
    url(r'^add_(\d+)_(\d+)$', views.add, name='add'),#第一个是商品的id，第二个是商品的数量

    url(r'^edit_(\d+)_(\d+)$', views.edit, name='edit'),  # 更新商品 第一个是商品的id，第二个是商品的数量
    url(r'^delete(\d+)$', views.delete, name='delete'),  #删除商品


]