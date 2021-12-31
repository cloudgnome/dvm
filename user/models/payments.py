from django.db import models
from user.models import User

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    positive = models.BooleanField(default=0)
    summ = models.PositiveIntegerField()

    @property
    def type(self):
        return "up" if self.positive else "down"