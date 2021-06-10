# Generated by Django 2.2.19 on 2021-06-10 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='Category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Category', to='auctions.Category'),
        ),
    ]