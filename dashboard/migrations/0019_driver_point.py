# Generated by Django 3.2.9 on 2022-01-01 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_delete_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_fname', models.CharField(max_length=50)),
                ('driver_lname', models.CharField(max_length=50)),
                ('driver_cnic', models.IntegerField()),
                ('driver_num', models.IntegerField()),
                ('driver_address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_name', models.CharField(max_length=10)),
            ],
        ),
    ]
