from django.db import models

# Create your models here.
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# accounts/models.py
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("sales_manager", "Sales Manager"),
        ("sales_executive", "Sales Executive"),
    ]

    email = models.EmailField(unique=True , blank=False, null=False)
    phone_no = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="sales_executive")
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    profile_pic = models.ImageField(upload_to="profile_pic/", blank=False, null=False, default="default_profile_pic.jpg")

    def save(self, *args, **kwargs):
        if self.is_superuser:   # always enforce
            self.role = "admin"
        super().save(*args, **kwargs)

    def __str__(self):
        
        return f"{self.username} ({self.role})"
    
    class abc(models.Model):
        # This class is not used, but it can be used for future extensions
        name = models.CharField(max_length=100)
        
