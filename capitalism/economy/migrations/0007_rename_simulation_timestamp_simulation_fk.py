# Generated by Django 3.2.9 on 2022-02-05 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0006_auto_20220204_1921'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timestamp',
            old_name='simulation',
            new_name='simulation_FK',
        ),
    ]