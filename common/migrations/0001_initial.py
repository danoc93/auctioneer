# Generated by Django 3.0 on 2020-04-11 22:24

import common.models.AuctionStatus
import common.models.Currency
import common.models.ItemCondition
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_ask_amount', models.FloatField(default=0)),
                ('expiration_time_utc', models.DateTimeField()),
                ('international_delivery', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'auction',
            },
        ),
        migrations.CreateModel(
            name='AuctionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(choices=[(common.models.AuctionStatus.AuctionStatusOption['OPEN'], 'open'), (common.models.AuctionStatus.AuctionStatusOption['CLOSED'], 'closed'), (common.models.AuctionStatus.AuctionStatusOption['FULFILLED'], 'fulfilled')], max_length=20, unique=True)),
            ],
            options={
                'db_table': 'auction_status',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=125, unique=True)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(choices=[(common.models.Currency.CurrencyOptions['USD'], 'usd'), (common.models.Currency.CurrencyOptions['GBP'], 'gbp')], max_length=5, unique=True)),
            ],
            options={
                'db_table': 'currency',
            },
        ),
        migrations.CreateModel(
            name='ItemCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(choices=[(common.models.ItemCondition.ItemConditionOptions['NEW'], 'new'), (common.models.ItemCondition.ItemConditionOptions['USED'], 'used')], max_length=20, unique=True)),
            ],
            options={
                'db_table': 'item_condition',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.CharField(max_length=60, unique=True)),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('registration_date_utc', models.DateTimeField()),
                ('city_name', models.TextField(max_length=150)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Country')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=125)),
                ('description', models.TextField(max_length=5000)),
                ('registration_date_utc', models.DateTimeField(default=django.utils.timezone.now)),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.ItemCondition')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.User')),
            ],
            options={
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_amount', models.FloatField()),
                ('bid_time_utc', models.DateTimeField()),
                ('is_winning_bid', models.BooleanField(default=False)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Auction')),
                ('bid_currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Currency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.User')),
            ],
            options={
                'db_table': 'bid',
            },
        ),
        migrations.AddField(
            model_name='auction',
            name='ask_amount_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Currency'),
        ),
        migrations.AddField(
            model_name='auction',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Item'),
        ),
        migrations.AddField(
            model_name='auction',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.AuctionStatus'),
        ),
    ]
