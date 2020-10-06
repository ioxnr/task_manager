from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Task(models.Model):
    NEW = 0
    PLANNED = 1
    IN_WORK = 2
    DONE = 3
    STATUS_CHOICES = (
        (NEW, 'Новая'),
        (PLANNED, 'Запланированная'),
        (IN_WORK, 'В работе'),
        (DONE, 'Завершенная')
    )
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    done_date = models.DateField(default=date.today)
    assignee = models.ForeignKey(Account, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.title

