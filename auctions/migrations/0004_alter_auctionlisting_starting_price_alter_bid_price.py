# Generated by Django 4.1.6 on 2023-02-11 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auctionlisting_category_auctionlisting_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='starting_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='bid',
            name='price',
            field=models.FloatField(),
        ),
    ]