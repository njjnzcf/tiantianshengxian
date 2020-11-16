#coding=utf-8


from hashlib import sha1

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render

from . import user_decorator
from .models import UserInfo
from df_goods.models import GoodsInfo


def register(request):
    return render(request, 'tt_user/register.html')


def login(request):

    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name':0, 'error_pwd': 0, 'uname':uname}
    return render(request, 'tt_user/login.html',context)


def check_username(request,username):
    count = UserInfo.objects.filter(uname=username)

    print (count)
    #return JsonResponse({'count': count})
    return HttpResponse(count)

def register_handle(request):
    user_name = request.POST.get('user_name')
    pwd = request.POST.get('pwd')
    cpwd = request.POST.get('cpwd')
    email = request.POST.get('email')
    print ('user=%s,pwd=%s,cpwd=%s'%(user_name,pwd,cpwd))
    if pwd != cpwd:
        return redirect('register')

    s1 = sha1()
    s1.update(pwd)
    upwd = s1.hexdigest()

    user = UserInfo()
    user.uname = user_name
    user.upwd = upwd
    user.uemail = email
    user.save()

    context = {}
    return render(request, 'tt_user/login.html', context)



def login_handle(request):
    post = request.POST
    username = post.get('username')
    username = '%s' %username
    pwd = post.get('pwd')
    print (username)
    jizhu = post.get('jizhu')
    print ('jizhu=%s'%jizhu)
    user = UserInfo.objects.filter(uname=username)
    print (user)
    if len(user) == 1:
        s1 = sha1()
        s1.update(pwd)
        if s1.hexdigest() == user[0].upwd:
            print ('密码蒸汽。。。')
            url = request.COOKIES.get('url','df_goods/index')
            red = HttpResponseRedirect(url)
            if None!=jizhu:
                print ('记住密码。。。')
                red.set_cookie('uname', username)
            else:
                print ('不需要记住密码。。。')
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = user[0].id
            print ('save session=============')
            request.session['user_name'] = username
            return red
        else:
            print ('密码不正确。。。')
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd':1, 'uname':username, 'upwd': pwd}
            return render(request, 'tt_user/login.html', context)
    else:
        print ('没有找到。。。')
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd':0, 'uname':username, 'upwd': pwd}
        return render(request,'tt_user/login.html', context)



def info(request):

    user_id = request.session.get('user_id','')
    user = UserInfo.objects.get(id=user_id)
    #获取浏览记录
    goods_ids = request.COOKIES.get('goods_ids','')
    print (goods_ids)
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    for goods_id in goods_ids1:

        goods_list.append(GoodsInfo.objects.get(pk=goods_id))

    context = {
        'title': '用户中心',
        'user': user,
        'page_name':1,
        'goods_list': goods_list
    }
    return render(request, 'tt_user/user_center_info.html', context)
