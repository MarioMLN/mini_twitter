from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):

    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    followers = models.ManyToManyField(
        "user.User",
        related_name='followers',
        null=True,
        blank=True,
        editable=False
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username
