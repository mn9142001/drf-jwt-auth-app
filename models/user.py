from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):

    @property
    def is_teacher(self):
        return self.user_type == self.UserTypes.TEACHER
    
    @property
    def is_student(self):
        return self.user_type == self.UserTypes.STUDENT