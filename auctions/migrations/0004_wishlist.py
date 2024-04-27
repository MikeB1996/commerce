# Generated by Django 5.0.2 on 2024-04-17 13:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auction_listings_userid_alter_bids_listingid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemid', models.ManyToManyField(to='auctions.auction_listings')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wisher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]