# Generated by Django 5.0.2 on 2024-04-25 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auction_listings_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listings',
            name='startingprice',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]