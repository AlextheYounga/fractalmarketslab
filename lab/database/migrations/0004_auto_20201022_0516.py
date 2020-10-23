# Generated by Django 3.0.3 on 2020-10-22 05:16

from django.db import migrations
import json
import sys
from ...shared.functions import *
from ...shared.imports import parseCSV


def build_stock_list():
    nasdaq = {'Nasdaq Composite': parseCSV('NasdaqComposite.csv')}
    nasdaq['Nasdaq Composite'].update(parseCSV('NasdaqOthersListed.csv'))
    dow = {'Dow Jones Industrial Average': parseCSV('DowJones.csv')}
    nyse = {'New York Stock Exchange': parseCSV('NYSE.csv')}
    russell2k = {'Russell 2000': parseCSV('Russell2000.csv')}
    russell3k = {'Russell 3000': parseCSV('Russell3000.csv')}
    spx = {'S&P 500': parseCSV('S&P500.csv')}

    stocks = [
        nasdaq,
        dow,
        nyse,
        russell2k,
        russell3k,
        spx
    ]

    return stocks


def index_stock_table_seeder(apps, schema_editor, stocks=build_stock_list()):
    Index = apps.get_model('database', 'Index')
    Stock = apps.get_model('database', 'Stock')
    for i, indices in enumerate(stocks):
        for index, stocks in indices.items():
            index_record = Index(
                name=index,
                count=len(stocks)
            )
            index_record.save()

            for i, row in stocks.items():
                Stock(
                    index_id=index_record,
                    ticker=row['ticker'],
                    name=row['name'],
                ).save()


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20201022_0435'),
    ]

    operations = [
        migrations.RunPython(index_stock_table_seeder)
    ]