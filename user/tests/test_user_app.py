from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from user.models import Follow


class UserRegistrationTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_user_registration(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "strongpassword123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_user_registration(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["password"][0].code, "password_too_short")


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="strongpassword123"
        )
        self.login_url = reverse('login')

    def test_user_login(self):
        data = {
            "username": "testuser",
            "password": "strongpassword123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_fail_user_login(self):
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FollowUnfollowTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="password123"
        )
        self.follow_url = reverse('follow', args=[self.user2.id])
        self.unfollow_url = reverse('follow', args=[self.user2.id])
        self.client.force_authenticate(user=self.user1)

    def test_follow_user(self):
        response = self.client.post(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Follow.objects.count(), 1)
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

    def test_unfollow_user(self):
        Follow.objects.create(follower=self.user1, following=self.user2)
        response = self.client.delete(self.unfollow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Follow.objects.count(), 0)