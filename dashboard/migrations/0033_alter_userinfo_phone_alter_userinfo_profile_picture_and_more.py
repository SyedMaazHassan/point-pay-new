# Generated by Django 4.0 on 2022-07-11 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0032_alter_userinfo_options_alter_userinfo_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='phone',
            field=models.CharField(blank=True, error_messages={'unique': 'User with this phone number already exists.'}, max_length=17, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='profile_picture',
            field=models.ImageField(default='dp/profile.jpg', upload_to='dp'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uid',
            field=models.CharField(blank=True, error_messages={'unique': 'User with this UID number already exists.'}, max_length=20, null=True, unique=True),
        ),
    ]
