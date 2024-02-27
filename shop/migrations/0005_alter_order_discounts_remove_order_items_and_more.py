# Generated by Django 5.0.2 on 2024-02-26 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_tax_stripe_id_alter_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discounts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_discounts', to='shop.discount'),
        ),
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AlterField(
            model_name='order',
            name='taxes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_taxes', to='shop.tax'),
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='order_items', to='shop.item'),
        ),
    ]