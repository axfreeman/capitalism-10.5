# Generated by Django 3.2.9 on 2022-02-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0009_simulation_parameter_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation_parameter',
            name='name',
            field=models.CharField(default='Initial', max_length=50),
        ),
    ]
