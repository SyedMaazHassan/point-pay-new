# Generated by Django 4.0 on 2022-08-23 14:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0033_alter_userinfo_phone_alter_userinfo_profile_picture_and_more'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_expired', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.userinfo')),
            ],
        ),
    ]
