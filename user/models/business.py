from django.db import models
from user.models import User

class Business(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    country = models.CharField(max_length=25)
    postal_code = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    website = models.CharField(max_length=255)