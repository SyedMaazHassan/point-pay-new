# Generated by Django 4.0 on 2022-08-24 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_account_account_id_transaction_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
