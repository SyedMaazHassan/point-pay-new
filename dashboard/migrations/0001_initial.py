# Generated by Django 2.2.10 on 2021-08-14 03:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(null=True, upload_to='dp')),
                ('added_at', models.DateTimeField(default=datetime.datetime(2021, 8, 14, 3, 38, 57, 369307, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(default='organization', max_length=15)),
                ('abbr', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=15)),
                ('logo', models.ImageField(upload_to='logo')),
                ('founded_in', models.DateField()),
                ('added_at', models.DateTimeField(default=datetime.datetime(2021, 8, 14, 3, 38, 57, 369307, tzinfo=utc))),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('code', models.CharField(max_length=255)),
                ('month', models.CharField(max_length=10)),
                ('year', models.IntegerField()),
                ('qr_code_picture', models.ImageField(null=True, upload_to='qr')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2021, 8, 14, 3, 38, 57, 369307, tzinfo=utc))),
                ('is_expired', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.OrgAdmin')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='orgadmin',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Organization'),
        ),
        migrations.AddField(
            model_name='orgadmin',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
