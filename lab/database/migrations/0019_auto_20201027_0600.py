# Generated by Django 3.0.3 on 2020-10-27 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0018_stock_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='ticker',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
