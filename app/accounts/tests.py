from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class AccountViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ali', password='12345', email='old@example.com')

    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'LOGIN')

    def test_profile_page_renders_for_logged_in_user(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('accounts:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile Details')

    def test_profile_update_persists_user_data(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('accounts:profile'),
            {
                'first_name': 'Ali',
                'last_name': 'Valiyev',
                'email': 'ali@example.com',
                'bio': 'Fresh products lover',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('accounts:profile'))
        self.user.refresh_from_db()
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(self.user.first_name, 'Ali')
        self.assertEqual(self.user.last_name, 'Valiyev')
        self.assertEqual(self.user.email, 'ali@example.com')
        self.assertEqual(profile.bio, 'Fresh products lover')
