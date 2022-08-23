from email.policy import default
import imp
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from random import randint
from itertools import chain
import qrcode
import datetime
import uuid
from dashboard.models import Voucher, UserInfo
# Create your models here.


# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

class VoucherUser(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        abstract = True


class FeeSubmission(VoucherUser):
    card = models.ImageField(upload_to = "cards", default="cards/test-card.jpg")


class Account(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Transaction(models.Model):
    amount = models.FloatField()
    signed_amount = models.FloatField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    fee_submission = models.ForeignKey(FeeSubmission, on_delete=models.CASCADE)
    is_credit = models.BooleanField(default=False)
    is_debit = models.BooleanField(default=False)
    source = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)


class RequestConfirmation(VoucherUser):
    signature = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        from django.conf import settings
        current_time = timezone.now()
        time_diff = current_time - self.created_at
        diff_in_secs = time_diff.total_seconds()
        diff_in_mins = diff_in_secs / 60
        return not diff_in_mins <= settings.PAYMENT_SESSION_EXPIRY_MIN

