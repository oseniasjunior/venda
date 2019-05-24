from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from core import models, tasks


@receiver(post_save, sender=models.SaleItem, dispatch_uid="update_subtotal", weak=False)
def update_subtotal(sender, instance: models.SaleItem, created=False, **kwargs):
    if created:
        subtotal = instance.product.sale_price * instance.quantity
        instance.subtotal = subtotal
        instance.save()


@receiver(post_save, sender=models.Sale, dispatch_uid="generate_movement_stock", weak=False)
def generate_movement_stock(sender, instance: models.Sale, created=False, **kwargs):
    if created:
        tasks.generate_movement_stock.apply_async([instance.id], countdown=2)


@receiver(post_save, sender=models.SaleItem, dispatch_uid="generate_movement_stock_item", weak=False)
def generate_movement_stock_item(sender, instance: models.SaleItem, created=False, **kwargs):
    if created:
        tasks.generate_movement_stock_item.apply_async([instance.id], countdown=5)
