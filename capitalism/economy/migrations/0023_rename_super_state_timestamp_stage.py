# Generated by Django 3.2.9 on 2022-01-15 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0022_auto_20220115_1028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timestamp',
            old_name='super_state',
            new_name='stage',
        ),
    ]
