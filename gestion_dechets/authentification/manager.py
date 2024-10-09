from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)
    
    def create_citoyen(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_citoyen', True)
        return self.create_user(username, email, password, **extra_fields)
    
    def create_entreprise(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_entreprise', True)
        return self.create_user(username, email, password, **extra_fields)
    
    def create_municipalite(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_municipalite', True)
        return self.create_user(username, email, password, **extra_fields)
