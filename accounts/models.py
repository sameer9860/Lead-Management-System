from django.db import models

# Create your models here.
# accounts/models.py
from django.contrib.auth.models import AbstractUser

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
    
    
class OTP(models.Model):    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    @staticmethod
    def generate_otp(email, length=8):
        import random

        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise Exception("User does not exist")

        # try to generate a unique otp at most 3 times
        for _ in range(3):
            otp = "".join(str(random.randint(0, 9)) for _ in range(length))
            if not OTP.objects.filter(otp=otp).exists():
                break

        new_otp = OTP(user=user, otp=otp)
        new_otp.save()

        return new_otp.otp

    def is_expired(self):
        from django.utils import timezone
        import datetime

        now = timezone.now()
        return now - self.created_at > datetime.timedelta(minutes=10)

    @staticmethod
    def check_otp(otp_value):
        otp_record = OTP.objects.filter(otp=otp_value).first()
        if otp_record and not otp_record.is_expired():  # otp is valid and used
            user_id = otp_record.user.id
            otp_record.delete()
            return user_id
        return None

    def __str__(self):
        return self.otp
    

        
