# Generated by Django 3.0.4 on 2020-03-21 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecasts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hourlyforecast',
            name='unformatted_time',
            field=models.IntegerField(default=1584755666.4101841),
        ),
        migrations.AddField(
            model_name='search',
            name='unformatted_time_of_search',
            field=models.IntegerField(default=1584755666.4097714),
        ),
    ]
