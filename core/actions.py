from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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


def send_channel_message(group_name: str, content: dict) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name, {
        "type": "group.message",
        "content": content
    })
