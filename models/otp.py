from django.db import models
from .user import User
from string import digits
import random

class OTP(models.Model):
    user = models.ForeignKey(User, models.Case)
    created_at = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(blank=True, max_length=12)
    
    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = "".join(random.choices(digits, k=6))
        return super().save(*args, **kwargs)