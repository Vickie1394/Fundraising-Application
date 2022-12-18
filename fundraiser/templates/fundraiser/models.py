from urllib import request
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from cloudinary import uploader, api
from cloudinary.models import CloudinaryField

sportsChoices = (
    ("football", "football"),
    ("basketball", "basketball"),
    ("tennis", "tennis"),
    ("ice hockey", "ice hockey"),
    ("handball", "handball"),
    ("rugby", "rugby"),
)

seriesChoices = (
    ("1.1 odds for 30 days", "1.1 odds for 30 days"),
)

betStatus = (
    ("won", "won"),
    ("lost", "lost"),
    ("void", "void"),
    ("pending", "pending"),
    ("refund", "refund")
)

paymentStatus = (
    ("successful", "successful"),
    ("pending", "pending"),
    ("denied", "denied"),
)

memberships = (
    ("Gold", "Gold"), # 1000
    ("Silver", "Silver"), # 850
    ("Bronze", "Bronze"), # 350
)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    id_number = models.CharField(max_length=9)
    account_balance = models.CharField(max_length = 12, default=0)
    my_qrcode = CloudinaryField('image', null=True)

class LatestTransaction(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    amount_recieved = models.CharField(max_length=10)
    senders_name = models.CharField(max_length=200)
    seen = models.BooleanField(default=False)


class Transaction(models.Model):
    prof = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount_received = models.CharField(max_length=20)
    senders_name = models.CharField(max_length=200)
    seen = models.BooleanField(default=False)


class LocalAgent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agent_number = models.CharField(max_length=20)
    business_name = models.CharField(max_length=1000)
    business_certificate = CloudinaryField('image')
    address = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=30)


class LocalAgentAccount(models.Model):
    local_agent = models.ForeignKey(LocalAgent,on_delete=models.CASCADE)
    float_balance = models.CharField(max_length=10, default = 0)


class LockSavingsAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_balance = models.CharField(max_length=20, default = 0)

class SchoolFeesSavings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_balance = models.CharField(max_length=20, default = 0)


class SchoolAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school_code = models.CharField(max_length = 50)
    school_name = models.CharField(max_length = 1000)
    account_balance = models.CharField(max_length=20)