# Generated by Django 4.0 on 2022-08-24 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0033_alter_userinfo_phone_alter_userinfo_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='status',
            field=models.CharField(choices=[('student', 'Student'), ('admin', 'Admin')], max_length=255),
        ),
    ]
