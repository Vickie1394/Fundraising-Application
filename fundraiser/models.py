from django.db import models
from django.contrib.auth.models import User, AbstractUser

class FundraisingEvent(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    name = models.TextField(max_length=500)
    intent = models.TextField(max_length=500)
    description = models.TextField(max_length=5000)
    start_date = models.DateField()
    end_date = models.DateField()
    target_amount = models.CharField(max_length = 20)
    amount_contributed = models.CharField(max_length=20, default=0)
    active = models.BooleanField(default=True)
    members = models.ManyToManyField(User, related_name="event_members")


class Contribution(models.Model):
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    fundraising_event = models.ForeignKey(FundraisingEvent, on_delete=models.CASCADE)
    amount = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
    mpesa_transaction_code = models.CharField(max_length=50)

