from django.db import models
from django.contrib.auth.models import AbstractUser,User
import random

class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(blank="True")
    employee_type= models.CharField(blank="False", default="Employee",max_length=10)
    employee_code = models.CharField(max_length=10, unique="True")
    image = models.ImageField(upload_to='images/',blank="True")

    def save(self,*args,**kwargs):
        if not self.employee_code:
            random_number = random.randint(100, 999)
            self.employee_code = f"EMP00{random_number}"
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name