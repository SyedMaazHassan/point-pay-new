# Generated by Django 3.2.9 on 2022-03-12 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuttles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shuttle',
            name='id_number',
            field=models.IntegerField(default=0),
        ),
    ]
