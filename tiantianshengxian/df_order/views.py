#coding=utf-8
from datetime import datetime
from decimal import Decimal

from django.db import transaction
from django.shortcuts import render, redirect
from df_cart.models import CartInfo
from df_user.models import UserInfo

from .models import OrderInfo, OrderDetailInfo


def order(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    ids = request.GET.getlist('id')
    #cart_ids=[int(item) for item in ids]
    carts = CartInfo.objects.filter(id__in=ids)


    context = {
        'title': '提交订单',
        'carts':carts,
        'page_name': 1,
        'user':user,
        'cart_ids': ','.join(ids)
    }
    return render(request, 'df_order/place_order.html', context)


@transaction.atomic()
def order_handle(request):
    tran_id=transaction.savepoint()
    cart_ids=request.POST.get('cart_ids')
    try:
        order= OrderInfo()
        now=datetime.now()
        uid= request.session['user_id']
        order.oid='%s%d'%(now.strftime('%Y%m%d%n%M%s'),uid)
        order.user_id=uid
        order.odate=now
        order.otatal=Decimal(request.POST.get('total'))
        order.save()
        cart_ids1=[int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids1:
            detail=OrderDetailInfo()
            detail.order=order
            cart=CartInfo.objects.get(id=id1)
            goods=cart.goods
            if goods.gkucun>=cart.count:
                goods.gkucun=cart.goods.gkucun-cart.count
                goods.save()

                detail.goods_id=goods.id
                detail.price=goods.gprice
                detail.count=cart.count
                detail.save()
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/df_cart/cart')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        transaction.savepoint_rollback(tran_id)
    return redirect('/user/order')
