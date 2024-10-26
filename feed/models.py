from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
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


class PostContent(models.Model):
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE
    )
    text = models.CharField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = _("PostContent")
        verbose_name_plural = _("PostContents")

    def __str__(self):
        return f"PostContents - {self.post.user.username}"


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
