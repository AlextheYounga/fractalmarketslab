# Generated by Django 3.0.3 on 2020-11-30 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0034_auto_20201130_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='macrotrend',
            name='ticker',
            field=models.CharField(max_length=30),
        ),
    ]
