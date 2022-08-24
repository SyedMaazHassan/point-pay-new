# Generated by Django 4.0 on 2022-08-24 09:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_remove_account_acc_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
