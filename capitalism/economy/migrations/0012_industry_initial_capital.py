# Generated by Django 3.2.9 on 2021-12-31 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0011_remove_timestamp_sub_state_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='industry',
            name='initial_capital',
            field=models.FloatField(default=0),
        ),
    ]
