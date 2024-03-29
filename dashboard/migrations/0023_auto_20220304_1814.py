# Generated by Django 3.2.9 on 2022-03-04 13:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_alter_voucher_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='driver_fname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='driver_lname',
            new_name='last_name',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='driver_num',
        ),
        migrations.AddField(
            model_name='driver',
            name='phone',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AddField(
            model_name='driver',
            name='profile_picture',
            field=models.ImageField(default='profile-pictures/drivers/default-dp.png', upload_to='profile-pictures/drivers'),
        ),
    ]
