from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name="following_set",
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name="followers_set",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower} follows {self.following}"

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("Você não pode seguir a si mesmo.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
