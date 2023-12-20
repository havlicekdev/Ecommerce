# Generated by Django 5.0 on 2023-12-16 17:27

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_message'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=datetime.datetime(2023, 12, 16, 18, 27, 34, 838846))),
                ('status', models.CharField(choices=[('PR', 'Přijato'), ('ZA', 'Zaplaceno'), ('OD', 'Odesláno'), ('FA', 'Fakturováno')], default='PR', max_length=20)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order_items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(max_length=200)),
                ('product_price', models.IntegerField()),
                ('product_quantity', models.IntegerField()),
                ('product_item_price', models.IntegerField()),
                ('product_category', models.CharField(max_length=200)),
                ('product_description', models.CharField(max_length=200)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='shop.product')),
            ],
        ),
    ]
