from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from feed.models import Post
from user.models import Follow


class PostTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="strongpassword123"
        )
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.user.delete()

    def test_create_post(self):
        data = {
            "text": "Good Morning!"
        }
        response = self.client.post(reverse('post'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], data['text'])
        self.assertTrue(Post.objects.filter(text=data['text'], user=self.user).exists())

    def test_update_post(self):
        self.post = Post.objects.create(text="Good Morning!", user=self.user)
        self.post_url = reverse('post', kwargs={'pk': self.post.pk})
        data = {
            "text": "Good Evening!"
        }
        response = self.client.patch(self.post_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        self.post = Post.objects.create(text="Good Morning!", user=self.user)
        self.post_url = reverse('post', kwargs={'pk': self.post.pk})
        response = self.client.delete(self.post_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_get_post(self):
        self.post = Post.objects.create(text="Good Morning!", user=self.user)
        self.post_url = reverse('post', kwargs={'pk': self.post.pk})
        response = self.client.get(self.post_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.post.text)


class UserFeedTestCase(APITestCase):
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
        self.client.force_authenticate(user=self.user1)

        Follow.objects.create(follower=self.user1, following=self.user2)
        data = {
            "text": "User2's post"
        }
        self.client.post(reverse('post'), data, format='json')

        self.feed_url = reverse('feed')

    def test_view_feed(self):
        response = self.client.get(self.feed_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['text'], "User2's post")


class LikeViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="password123"
        )
        post_author = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

        self.post = Post.objects.create(text="Good Morning!", user=post_author)

        self.likes_url = reverse('likes', kwargs={'post_pk': self.post.pk})

    def test_like_post(self):
        response = self.client.post(self.likes_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def retrieve_post_with_a_like(self):
        self.client.post(self.likes_url)

        post_url = reverse('post', kwargs={'pk': self.post.pk})
        response = self.client.get(post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['like_count'], 1)
