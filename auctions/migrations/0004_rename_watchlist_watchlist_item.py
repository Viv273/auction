# Generated by Django 3.2.9 on 2022-01-15 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='watchlist',
            new_name='item',
        ),
    ]
