#coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import CartInfo


def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'title': '购物车',
        'page_name': 1,
        'carts': carts,
    }
    if request.is_ajax():
        return JsonResponse(context)
    else:
        return render(request, 'df_cart/cart.html', context)

#添加购物车
def add(request, gid, count):
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    #查询购物车中是否已经含有该商品，如果有就增加数量  如果没有就新增数据
    carts = CartInfo.objects.filter(user_id=uid,goods_id=gid)

    if len(carts)>=1:
        cart = carts[0]
        cart.count =cart.count+count

    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id =gid
        cart.count = count
    cart.save()
    #如果是ajax请求就返回json，否在跳转购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        print ('count=%s'%count)
        return JsonResponse({'count': count})
    else:
        return redirect('/df_cart/cart')


#删除数据
def delete(request, id):
    try:
        cart = CartInfo.objects.get(pk=int(id))
        cart.delete()
        data = {
            'ok':1
        }
    except Exception as e:
        data = {'ok':0}
    return JsonResponse(data)



#更新
def edit(request, cart_id, count):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        count1 = cart.count = int(count)
        cart.save()
        data= {'ok':0}
    except Exception as e:
        data= {'ok':count1}
    return JsonResponse(data)


