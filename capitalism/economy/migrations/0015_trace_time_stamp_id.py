# Generated by Django 3.2.9 on 2022-02-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0014_auto_20220212_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='trace',
            name='time_stamp_id',
            field=models.IntegerField(default=0),
        ),
    ]
