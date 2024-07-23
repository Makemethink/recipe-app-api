from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Super user needs to have is_staff = True")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super user needs to have is_superuser = True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):

    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField(null=True)

    # Telling django to use the specified Manager for the User to create user
    objects = CustomUserManager()

    # REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.username
