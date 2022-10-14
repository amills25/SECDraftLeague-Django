import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class UserMembership(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    membership_id = models.IntegerField()

class Membership(models.Model):
    id = models.ManyToManyField(UserMembership)
    label = models.CharField(max_length=20)

class Athlete(models.Model):
    name = models.CharField(max_length=50)
    team = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)

class Week(models.Model):
    athlete_id = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    lineup_id = models.IntegerField()
    points = models.IntegerField()
    week_number = models.IntegerField()

class Lineup(models.Model):
    id = models.ManyToManyField(Week)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
