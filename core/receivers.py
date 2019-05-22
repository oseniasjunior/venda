from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from core import models


@receiver(post_save, sender=models.SaleItem, dispatch_uid="update_subtotal", weak=False)
def update_subtotal(sender, instance: models.SaleItem, created=False, **kwargs):
    if created:
        subtotal = instance.product.sale_price * instance.quantity
        instance.subtotal = subtotal
        instance.save()


@receiver(post_save, sender=models.Sale, dispatch_uid="generate_movement_stock", weak=False)
def generate_movement_stock(sender, instance: models.Sale, created=False, **kwargs):
    if created:
        stock_address, created = models.StockAddress.objects.get_or_create(description='SAIDA')
        try:
            models.MovementStock.objects.get(document=instance.pk)
        except models.MovementStock.DoesNotExist:
            payload = {
                'type': models.MovementStock.OUT,
                'date': now().date(),
                'stock_address': stock_address,
                'document': str(instance.id)
            }
            models.MovementStock.objects.create(**payload)


@receiver(post_save, sender=models.SaleItem, dispatch_uid="generate_movement_stock_item", weak=False)
def generate_movement_stock_item(sender, instance: models.SaleItem, created=False, **kwargs):
    if created:
        movement_stock = models.MovementStock.objects.get(document=instance.sale.pk)
        payload = {
            'movement_stock': movement_stock,
            'product': instance.product,
            'quantity': instance.quantity
        }
        models.MovementStockItem.objects.create(**payload)
