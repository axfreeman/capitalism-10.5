# Generated by Django 3.2.9 on 2022-01-28 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0011_auto_20220127_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='current_time_stamp',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_time_stamp', to='economy.timestamp'),
        ),
    ]