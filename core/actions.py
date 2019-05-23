from django.utils.timezone import now

from core import models


def generate_movement_stock(instance: models.Sale):
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


def generate_movement_stock_item(instance: models.SaleItem):
    movement_stock = models.MovementStock.objects.get(document=instance.sale.pk)
    payload = {
        'movement_stock': movement_stock,
        'product': instance.product,
        'quantity': instance.quantity
    }
    models.MovementStockItem.objects.create(**payload)
