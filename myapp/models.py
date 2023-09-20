from django.db import models
from django.contrib.auth.models import AbstractUser,User
import random
# from phonenumber_field.modelfields import PhoneNumberField 

class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(blank="True")
    employee_type= models.CharField(blank="False", default="Employee",max_length=10)
    employee_code = models.CharField(max_length=10, unique="True")
    image = models.ImageField(upload_to='images/',default='images/default-profile-pic.jpg',blank="False")
    phone_number=models.CharField(max_length=13,blank="True")

    def save(self,*args,**kwargs):
        if not self.employee_code:
            random_number = random.randint(100, 999)
            self.employee_code = f"EMP00{random_number}"
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name
    
class Messages(models.Model):
    messagefrom = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(blank=True, max_length=200)
    message = models.TextField(blank=True)
    attachment = models.FileField(blank=True)
    send_on = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False) 


    def __str__(self):
        return f"Message from {self.messagefrom} to {self.to}"