# Generated by Django 3.2.9 on 2022-05-28 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shuttles', '0003_rename_created_at_shuttle_added_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shuttle',
            options={'ordering': ('id',)},
        ),
    ]
