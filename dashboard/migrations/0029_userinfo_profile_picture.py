# Generated by Django 3.2.9 on 2022-07-11 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_remove_userinfo_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='profile_picture',
            field=models.ImageField(default='dp/default.jpg', upload_to='dp'),
        ),
    ]
