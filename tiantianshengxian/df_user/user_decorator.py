#coding=utf-8

#登录验证
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def login(func):
    def login_fun(request,*args, **kwargs):
        print ('==============login first============')
      #  if request.session.has_key('user_id'):
      #      return func(request, *args, **kwargs)
      #  else:
      #      red = HttpResponseRedirect('/user/login')
      #      red.set_cookie('url', request.get_full_path())
       #     return red
        return login_fun