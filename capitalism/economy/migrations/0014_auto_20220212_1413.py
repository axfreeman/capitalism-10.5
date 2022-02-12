# Generated by Django 3.2.9 on 2022-02-12 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0013_remove_user_current_time_stamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialstock',
            options={'ordering': ['commodity_FK__display_order'], 'verbose_name': 'Social Stock', 'verbose_name_plural': 'Social Stocks'},
        ),
        migrations.RemoveField(
            model_name='trace',
            name='time_stamp_id',
        ),
        migrations.AddField(
            model_name='trace',
            name='simulation_FK',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='economy.simulation'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='name',
            field=models.CharField(default='Undefined', max_length=50),
        ),
    ]
