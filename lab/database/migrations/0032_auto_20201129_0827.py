# Generated by Django 3.0.3 on 2020-11-29 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0031_auto_20201129_0819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalprices',
            options={'verbose_name': 'HistoricalPrice', 'verbose_name_plural': 'HistoricalPrices'},
        ),
    ]