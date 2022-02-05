# Generated by Django 3.2.9 on 2022-02-04 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0004_timestamp_simulation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timestamp',
            name='simulation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='economy.simulation_parameter'),
        ),
    ]
