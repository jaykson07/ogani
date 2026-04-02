from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from app.products.models import *
from .forms import OrderForm


# Create your views here.


def get_active_cart(user, create=False):
    cart = Cart.objects.filter(client=user, is_ordered=False).order_by('-id').first()
    if create and cart is None:
        cart = Cart.objects.create(client=user, is_ordered=False)
    return cart


@login_required
def cart(request):
    car = get_active_cart(request.user, create=True)
    ctx = {
        'cart': car
    }
    return render(request, 'shoping-cart.html', ctx)


@login_required
def add_wishlist(request):
    pid = request.GET.get('_pid')
    product = get_object_or_404(Product, id=pid)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    if wishlist_item is None:
        Wishlist.objects.create(user=request.user, product=product)
        data = {
            'success': True,
            'product': product.name,
            'message': 'successfully added your wishlist'
        }
    else:
        wishlist_item.delete()
        data = {
            'success': False,
            'product': product.name,
            'message': 'successfully removed from your wishlist'
        }
    return JsonResponse(data)


@login_required
def my_wishlist(request):
    my_wl = Wishlist.objects.filter(user=request.user).select_related('product', 'product__category')
    latest_products = Product.objects.order_by('-id')[:6]
    s = request.GET.get('s')
    if s:
        my_wl = my_wl.filter(product__name__icontains=s)
    cat = request.GET.get('cat')
    if cat:
        my_wl = my_wl.filter(product__category__category__exact=cat)
    ctx = {
        'products': my_wl,
        'latest_products': latest_products
    }
    return render(request, 'my-wishlist.html', ctx)


@login_required
def add_cart(request):
    pid = request.GET.get('_pid')
    product = get_object_or_404(Product, id=pid)
    my_cart = get_active_cart(request.user, create=True)

    count = CartItem.objects.filter(cart=my_cart, product=product).count()
    if count < 1:
        CartItem.objects.create(product=product, cart=my_cart)
        data = {
            'success': True,
            'product': product.name,
            'message': 'successfully added your cart!!!'
        }
    else:
        data = {
            'success': True,
            'product': product.name,
            'message': 'already your cart!!!'
        }
    return JsonResponse(data, status=201)


@login_required
def plus_quantity(request):
    cid = request.GET.get('_cid')
    cart_item = get_object_or_404(
        CartItem,
        id=cid,
        cart__client=request.user,
        cart__is_ordered=False,
    )
    cart_item.quantity += 1
    cart_item.save()
    data = {
        'success': True,
        'message': ' cart item incremented by 1',
    }
    return JsonResponse(data, status=200)


@login_required
def minus_quantity(request):
    cid = request.GET.get('_cid')
    cart_item = get_object_or_404(
        CartItem,
        id=cid,
        cart__client=request.user,
        cart__is_ordered=False,
    )
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        data = {
            'success': True,
        }
    else:
        cart_item.delete()
        data = {
            'success': True,
    }
    return JsonResponse(data, status=200)


@login_required
def delete_cart_item(request):
    pk = request.GET.get('_cid')
    get_object_or_404(
        CartItem,
        id=pk,
        cart__client=request.user,
        cart__is_ordered=False,
    ).delete()
    data = {
        'success': True
    }
    return JsonResponse(data, status=200)


@login_required
def checkout(request):
    cart_id = request.GET.get('cart_id')
    if cart_id:
        car = Cart.objects.filter(id=cart_id, client=request.user, is_ordered=False).first()
    else:
        car = get_active_cart(request.user)

    has_items = bool(car and car.cart_items.exists())
    if not has_items:
        ctx = {
            'form': OrderForm(),
            'cart': car,
            'is_empty_checkout': True,
        }
        return render(request, 'checkout.html', ctx)

    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.cart = car
        order.client = request.user
        order.save()
        car.is_ordered = True
        car.save()
        messages.success(request, 'Your order has been placed successfully.')
        return redirect('carts:cart')
    ctx = {
        'form': form,
        'cart': car,
        'is_empty_checkout': False,
    }
    return render(request, 'checkout.html', ctx)
