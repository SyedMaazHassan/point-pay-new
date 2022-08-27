from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from random import randint
from itertools import chain
import qrcode
import datetime
import uuid
from dashboard.models import Organization, Voucher, UserInfo
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.db.models import Sum
from django.conf import settings

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

    def get_formatted_date(self, date):
        return date.strftime("%b %d, %Y")

    def get_expiry_date(self):
        month = self.voucher.month
        year = self.voucher.year
        last_date = 28 if month == 2 else 30
        date_obj = datetime.datetime(year, month, last_date)
        return date_obj.strftime("%b %d, %y")


    def save(self, *args, **kwargs):
        if not self.pk:
            import cv2
            import os
            from dashboard.supporting_func import id_card_generate
            logo = os.path.join(settings.BASE_DIR, "media", str(self.voucher.organization.logo))
            user_profile = os.path.join(settings.BASE_DIR, "media", str(self.user.profile_picture))
            organization_logo = cv2.imread(logo)
            organization_abbr = self.voucher.organization.abbr
            department = 'CIS Department'
            fee_price = f'{settings.CURRENCY_SYMBOL} {self.voucher.price}'
            user_full_name = f'{self.user.user.first_name} {self.user.user.last_name}'
            roll_num = 'CS-18180'
            user_profile_pic = cv2.imread(user_profile)
            issue_date = self.get_formatted_date(timezone.now())
            expiry_date = self.get_expiry_date()

            new_card = id_card_generate(
                organization_logo,
                organization_abbr, 
                department, 
                fee_price,
                user_full_name,
                user_profile_pic,
                roll_num,
                issue_date,
                expiry_date
            )

            self.card.save(new_card['name'], new_card['content'], save=False)

        super(FeeSubmission, self).save(*args, **kwargs)


class Account(models.Model):
    account_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, null=True, blank = True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True, blank = True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank = True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} - {self.account_id}' 

    def is_enough_balance(self, required_amount):
        current_balance = self.balance_num()
        return current_balance >= required_amount

    def type(self):
        account_type = "Student" if self.user else "Organization"
        return f'{account_type} account'

    def balance_num(self):
        all_transaction_of_account = Transaction.objects.filter(account = self)
        agg_sum = all_transaction_of_account.aggregate(Sum("signed_amount"))
        agg_sum = agg_sum['signed_amount__sum'] if agg_sum['signed_amount__sum'] else 0
        return agg_sum

    def balance(self):
        acc_balance = self.balance_num()
        return f'{settings.CURRENCY_SYMBOL} {acc_balance}'

    def add_transaction(self, amount, source, note, is_credit = False, is_debit = False):
        if is_debit == is_credit:
            raise Exception("Transaction can't be added")
        signed_amount = amount if is_credit else amount*-1
        new_transaction = Transaction.objects.create(
            amount = amount,
            signed_amount = signed_amount,
            is_credit = is_credit,
            is_debit = is_debit,
            source = source,
            note = note,
            account = self
        )
        return new_transaction

    def credit(self, amount, source, note):
        return self.add_transaction(amount=amount, source=source, note=note, is_credit=True)

    def debit(self, amount, source, note):
        if self.is_enough_balance(amount):
            return self.add_transaction(amount=amount, source=source, note=note, is_debit=True)
        raise Exception("Wallet Topup required to do this transaction. Add balance by the option below.")

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.user and not self.organization:
                raise Exception("Account can't be created")
        super(Account, self).save(*args, **kwargs)


@receiver(post_save, sender=UserInfo)
def create_account(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                if instance.status == "student":
                    account = Account.objects.create(
                        title = f'{instance.user.first_name} {instance.user.last_name}', 
                        user = instance
                    )
                    account.credit(1000, "System", "Free credit provided by the system")
                
                elif instance.status == "admin":
                    account_check = Account.objects.filter(organization = instance.organization).first()
                    if not account_check:
                        account = Account.objects.create(
                            title = instance.organization.name,
                            organization = instance.organization
                        )  
        except:
            print("something went wrong")
            instance.delete()
            raise Exception("Error while creating the account. Try registering the user again.")
    print("nothing works")

class Transaction(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.FloatField()
    signed_amount = models.FloatField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    fee_submission = models.ForeignKey(FeeSubmission, on_delete=models.CASCADE, null = True, blank = True)
    is_credit = models.BooleanField(default=False)
    is_debit = models.BooleanField(default=False)
    source = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)


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