from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import *
from dashboard.models import Organization, UserInfo, Voucher
from payment.models import *








class FeeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeSubmission
        # fields = ["card"]
        exclude = ["id", "voucher", "user"]


class TransactionSerializer(serializers.ModelSerializer):
    fee_submission = FeeSubmissionSerializer(many = False)
    class Meta:
        model = Transaction
        # fields = ["card"]
        exclude = ["id", "account"]
