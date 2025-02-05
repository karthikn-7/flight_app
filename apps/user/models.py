from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class SimpleUserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None):
        """Creates and saves a user with an email, full name, and password."""
        if not email:
            raise ValueError("An email address is required")
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname)
        user.set_password(password)  # Hashes the password before saving
        user.save(using=self._db)
        return user

class SimpleUser(AbstractBaseUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    
    is_active = models.BooleanField(default=True)  # Allows users to log in

    objects = SimpleUserManager()

    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname"]

    def __str__(self):
        return self.fullname
