import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Inventoryandy(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    cost_per_item = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    quantity_in_stock = models.IntegerField(null=False, blank=False)
    quantity_sold = models.IntegerField(null=False, blank=False)
    remaining_quantity = models.IntegerField(null=False, blank=False, default=0)
    sales = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False, default=0)
    stock_date = models.DateField(auto_now_add=True)
    last_sales_date = models.DateField(auto_now=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Changed to CharField

    def __str__(self) -> str:
        return self.name

    def calculate_sales(self):
        return self.cost_per_item * self.quantity_sold

    def calculate_remaining_quantity(self):
        return self.quantity_in_stock - self.quantity_sold

    def save(self, *args, **kwargs):
        self.sales = self.calculate_sales()
        self.remaining_quantity = self.calculate_remaining_quantity()
        super().save(*args, **kwargs)

@receiver(pre_save, sender=Inventoryandy)
def update_inventory(sender, instance, **kwargs):
    instance.sales = instance.calculate_sales()
    instance.remaining_quantity = instance.calculate_remaining_quantity()
