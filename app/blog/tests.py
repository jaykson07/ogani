from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from app.products.models import Category

from .models import Post, Tag


class BlogViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='blogger', password='12345')
        self.category = Category.objects.create(category='Food')
        self.tag = Tag.objects.create(tag='Healthy')
        self.post = Post.objects.create(
            author=self.user,
            title='Healthy food tips',
            image=SimpleUploadedFile('post.jpg', b'filecontent', content_type='image/jpeg'),
            category=self.category,
            content='Useful content',
            author_name='Blogger',
            author_image=SimpleUploadedFile('author.jpg', b'filecontent', content_type='image/jpeg'),
        )
        self.post.tags.add(self.tag)

    def test_blog_page_renders(self):
        response = self.client.get(reverse('blog:blog'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_blog_detail_page_renders(self):
        response = self.client.get(reverse('blog:blog-details', args=[self.post.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
