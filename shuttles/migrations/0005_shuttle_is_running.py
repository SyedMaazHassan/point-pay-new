# Generated by Django 4.0 on 2022-08-22 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuttles', '0004_alter_shuttle_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='shuttle',
            name='is_running',
            field=models.BooleanField(default=False),
        ),
    ]
