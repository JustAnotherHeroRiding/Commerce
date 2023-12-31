# Generated by Django 4.1.6 on 2023-02-12 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winning_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
