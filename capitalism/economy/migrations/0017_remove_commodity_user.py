# Generated by Django 3.2.9 on 2022-02-13 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0016_remove_trace_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commodity',
            name='user',
        ),
    ]