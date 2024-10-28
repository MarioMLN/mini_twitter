from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    text = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return f"Posts - {self.user.username}"

    @property
    def like_count(self):
        return Likes.objects.filter(post=self).count()


class Likes(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        verbose_name_plural = _("Likes")
        unique_together = ('user', 'post')

    def __str__(self):
        return "Likes"
