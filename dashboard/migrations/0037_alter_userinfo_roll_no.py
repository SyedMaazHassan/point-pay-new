# Generated by Django 4.0 on 2022-08-26 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0036_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='roll_no',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]