from django.shortcuts import render, get_object_or_404
from app.blog.models import Post
from .models import Product


# Create your views here.

def home(request):
    posts = Post.objects.order_by('-id')[:3]
    products = Product.objects.all().order_by('-id')
    top_rated_products = products.order_by('-mid_rate')[:6]
    top_viewed_products = products.order_by('-views')[:6]
    latest_products = products[:6]
    s = request.GET.get('s')
    if s:
        products = Product.objects.filter(name__icontains=s)
    ctx = {
        'products': products[:8],
        'posts': posts,
        'latest_products': latest_products,
        'top_rated_products': top_rated_products,
        'top_viewed_products': top_viewed_products,
    }
    return render(request, 'index.html', ctx)


def shop_details(request, pid):
    product = get_object_or_404(Product, id=pid)
    Product.objects.filter(id=pid).update(views=product.views + 1)
    product.refresh_from_db()
    related_products = Product.objects.order_by('-id')[:4]
    ctx = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'shop-details.html', ctx)


def shop_grid(request):
    products = Product.objects.order_by('-id')[:12]
    last_products = Product.objects.order_by('-id')[:6]
    s = request.GET.get('s')
    if s:
        products = Product.objects.filter(name__icontains=s)
    cat = request.GET.get('cat')
    if cat:
        products = Product.objects.filter(category__category__exact=cat)
    ctx = {
        'products': products,
        'last_products': last_products
    }
    return render(request, 'shop-grid.html', ctx)
