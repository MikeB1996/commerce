# Generated by Django 5.0.2 on 2024-04-25 11:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auction_listings_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listings',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Auctions_won', to=settings.AUTH_USER_MODEL),
        ),
    ]
