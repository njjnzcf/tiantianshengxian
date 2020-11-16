from django.shortcuts import render

def cart(request):
    return render(request, 'df_cart/cart.html')
