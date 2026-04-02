from django.test import TestCase
from django.urls import reverse

from app.products.models import Category

from .models import Contact, Subscribe


class ContactViewTests(TestCase):
    def setUp(self):
        Category.objects.create(category='Vegetables')
        self.url = reverse('contacts:contact')

    def test_contact_page_renders(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Leave Message')

    def test_contact_form_submission_creates_contact(self):
        response = self.client.post(
            self.url,
            {
                'name': 'Ali',
                'email': 'ali@example.com',
                'message': 'Salom, boglanish uchun yozdim.',
            },
            follow=True,
        )

        self.assertRedirects(response, self.url)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertContains(response, 'Your message has been sent successfully.')

    def test_subscribe_from_querystring_creates_subscription(self):
        response = self.client.get(self.url, {'email': 'sub@example.com'}, follow=True)

        self.assertRedirects(response, self.url)
        self.assertEqual(Subscribe.objects.count(), 1)
        self.assertContains(response, 'You have successfully subscribed.')

    def test_duplicate_subscribe_shows_info_message(self):
        Subscribe.objects.create(email='sub@example.com')

        response = self.client.get(self.url, {'email': 'sub@example.com'}, follow=True)

        self.assertRedirects(response, self.url)
        self.assertEqual(Subscribe.objects.count(), 1)
        self.assertContains(response, 'This email is already subscribed.')
