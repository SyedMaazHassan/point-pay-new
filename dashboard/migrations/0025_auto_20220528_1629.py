# Generated by Django 3.2.9 on 2022-05-28 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_delete_driver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='context',
        ),
        migrations.RemoveField(
            model_name='status',
            name='pages',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='uid',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='status',
            field=models.CharField(choices=[('student', 'Student'), ('admin', 'Admin'), ('driver', 'Driver')], max_length=255),
        ),
        migrations.DeleteModel(
            name='DataField',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
