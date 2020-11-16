from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register$', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^register_handle$', views.register_handle, name='register'),
    url(r'^check_username(\d+)$', views.check_username, name='check_username'),
    url(r'^handle_login$', views.login_handle, name='login_handle'),
    url(r'^user/info$', views.info, name='user_info'),




]
