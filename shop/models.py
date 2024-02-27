from decimal import Decimal, ROUND_HALF_UP

from django.db import models

CURRENCY = (
    ('usd', 'USD'),
    ('rub', 'RUB'),
)


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # доп поля
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY,
        default='rub',
    )
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_total_price(self):
        return self.price * self.quantity


class Discount(models.Model):
    name = models.CharField(max_length=200)
    value = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    def __str__(self):
        return f'Discount: {self.value}%'


class Tax(models.Model):
    name = models.CharField(max_length=200)
    percentage = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(
        Item, related_name='order_items'
    )
    discounts = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='order_discounts'
    )
    taxes = models.ForeignKey(
        Tax, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='order_taxes'
    )

    def __str__(self):
        return "Order №" + str(self.id)

    def get_total(self):
        total_items_sum = sum(
            [item.get_total_price() for item in self.items.all()]
        )
        total_price = total_items_sum * Decimal(1-(self.discounts.value/100))
        tax_percentage = Decimal(self.taxes.percentage) / Decimal(100)
        total_price_with_tax = total_price * Decimal(1 + tax_percentage)
        # подровнять запятую
        total_price_with_tax = total_price_with_tax.quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        return total_price_with_tax
