# Generated by Django 5.0.2 on 2024-04-19 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listings',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='bids',
            name='bidprice',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]