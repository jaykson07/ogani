from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from app.blog.models import Post, Tag

from .models import Category, Product
from .templatetags.cart_tag import featured_post_url, featured_product_url


class NavigationTagTests(TestCase):
    def test_featured_urls_fallback_to_list_pages(self):
        self.assertEqual(featured_product_url(), reverse('products:shop_grid'))
        self.assertEqual(featured_post_url(), reverse('blog:blog'))

    def test_featured_urls_point_to_latest_detail_pages(self):
        category = Category.objects.create(category='Fruits')
        product = Product.objects.create(
            name='Apple',
            category=category,
            price=12000,
            description='Fresh apple',
        )

        user = User.objects.create_user(username='ali', password='12345')
        tag = Tag.objects.create(tag='Food')
        post = Post.objects.create(
            author=user,
            title='Healthy food tips',
            image=SimpleUploadedFile('post.jpg', b'filecontent', content_type='image/jpeg'),
            category=category,
            content='Useful content',
            author_name='Ali',
            author_image=SimpleUploadedFile('author.jpg', b'filecontent', content_type='image/jpeg'),
        )
        post.tags.add(tag)

        self.assertEqual(featured_product_url(), reverse('products:shop-details', args=[product.id]))
        self.assertEqual(featured_post_url(), reverse('blog:blog-details', args=[post.id]))


class ProductViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category='Vegetables')
        self.product = Product.objects.create(
            name='Cucumber',
            category=self.category,
            price=9000,
            description='Fresh cucumber',
        )

    def test_shop_grid_is_public(self):
        response = self.client.get(reverse('products:shop_grid'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_shop_details_is_public(self):
        response = self.client.get(reverse('products:shop-details', args=[self.product.id]))

        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.views, 1)
