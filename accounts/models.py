from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Mymanager(BaseUserManager):
    def create_user(self, first_name,last_name, username, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name,last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,

            password=password,
        )
        user.is_admin = True

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, blank=True)
    username = models.CharField(verbose_name="Phone", max_length=30, unique=True)
    first_name = models.CharField(
         max_length=30, blank=True
    )
    last_name = models.CharField(
         max_length=30, blank=True
    )
    last_login = models.DateTimeField(verbose_name="last_login", auto_now=True)
    date_joined = models.DateTimeField(verbose_name="date_joined", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)
    is_bdo = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",

    ]
    objects = Mymanager()

    def __str__(self):
        return f"{self.first_name},{self.last_name},{self.username}"
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_lable):
        return True

        