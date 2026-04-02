from django import template
from django.urls import reverse

from app.blog.models import Post
from app.carts.models import Cart, Wishlist
from app.products.models import Category, Product

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_cart(context):
    request = context['request']
    user = request.user
    if not user.is_authenticated:
        return []
    cart = Cart.objects.filter(client=user, is_ordered=False).order_by('-id').first()
    if not cart:
        cart = []
    return cart


@register.simple_tag(takes_context=True)
def get_user_wishlist(context):
    request = context['request']
    user = request.user
    if not user.is_authenticated:
        return []
    wl = Wishlist.objects.filter(user=user)
    wlist_products = [product.product.id for product in wl]
    return wlist_products


@register.simple_tag()
def categories():
    return Category.objects.all()


@register.simple_tag()
def featured_product_url():
    product = Product.objects.order_by('-id').first()
    if product:
        return reverse('products:shop-details', args=[product.id])
    return reverse('products:shop_grid')


@register.simple_tag()
def featured_post_url():
    post = Post.objects.order_by('-id').first()
    if post:
        return reverse('blog:blog-details', args=[post.id])
    return reverse('blog:blog')
