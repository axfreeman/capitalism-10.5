# Generated by Django 3.2.9 on 2022-02-08 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0012_auto_20220207_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='current_time_stamp',
        ),
    ]