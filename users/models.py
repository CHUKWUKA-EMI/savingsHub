import datetime
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import jwt
from datetime import timedelta
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        """
        Create and save a user with the given names, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not first_name or not last_name:
            raise ValueError('First and Last name must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(f"{first_name}_{last_name}")
        user = self.model(username=username, email=email,first_name=first_name, last_name=last_name, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, first_name, last_name, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=50,blank=False)
    last_name = models.CharField(max_length=50,blank=False)
    password = models.CharField(null=False, max_length=128)
    phone_number = models.CharField(max_length=15)
    home_address = models.CharField(max_length=100)
    gender = models.CharField(max_length=6)
    employment_status = models.CharField(max_length=20)
    country = models.CharField(max_length=256, blank=False)
    date_of_birth = models.DateField(null=True, blank=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD ='email'
    REQUIRED_FIELDS =['first_name','last_name','country', 'date_of_birth']

    @property
    def token(self):
        auth_token = jwt.encode({'username': self.username,'email':self.email, 'exp':datetime.datetime.utcnow()+ timedelta(days=1)}, key=settings.JWT_SECRET_KEY, algorithm='HS256')
        return auth_token