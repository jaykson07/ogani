from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app.products.models import Category, Product

from .models import Cart, CartItem


class CartViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ali', password='12345')
        self.client.force_login(self.user)
        self.category = Category.objects.create(category='Vegetables')
        self.product = Product.objects.create(
            name='Tomato',
            category=self.category,
            price=15000,
            description='Fresh tomato',
        )
        self.cart = Cart.objects.create(client=self.user, is_ordered=False)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

    def test_cart_page_renders_quantity_controls(self):
        response = self.client.get(reverse('carts:cart'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'pro-qty')
        self.assertContains(response, 'delete-cart-item')

    def test_plus_quantity_increments_cart_item(self):
        response = self.client.get(reverse('carts:plus_quantity'), {'_cid': self.cart_item.id})

        self.assertEqual(response.status_code, 200)
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 2)

    def test_minus_quantity_decrements_cart_item(self):
        self.cart_item.quantity = 2
        self.cart_item.save()

        response = self.client.get(reverse('carts:minus_quantity'), {'_cid': self.cart_item.id})

        self.assertEqual(response.status_code, 200)
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 1)

    def test_minus_quantity_deletes_item_when_quantity_is_one(self):
        response = self.client.get(reverse('carts:minus_quantity'), {'_cid': self.cart_item.id})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(CartItem.objects.filter(id=self.cart_item.id).exists())

    def test_checkout_page_contains_wishlist_button_and_no_pages_wishlist_item(self):
        response = self.client.get(reverse('carts:checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'GO TO WISHLIST')
        self.assertContains(response, 'BACK TO CART')
        self.assertNotContains(
            response,
            f'<li><a href="{reverse("carts:my-wishlist")}">Wishlist</a></li>',
            html=True,
        )

    def test_empty_checkout_renders_without_redirect(self):
        self.cart_item.delete()

        response = self.client.get(reverse('carts:checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your checkout is empty')

    def test_checkout_success_redirects_to_cart(self):
        response = self.client.post(
            reverse('carts:checkout'),
            {
                'address': 'Tashkent',
                'phone': '+998901234567',
                'note': 'Call before delivery',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('carts:cart'))
        self.assertContains(response, 'Your order has been placed successfully.')
