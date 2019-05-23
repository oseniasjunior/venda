from celery import shared_task

from core import actions, models


@shared_task(queue='stock')
def generate_movement_stock(sale: int):
    instance = models.Sale.objects.get(pk=sale)
    actions.generate_movement_stock(instance=instance)


@shared_task(queue='stock')
def generate_movement_stock_item(sale_item: int):
    instance = models.SaleItem.objects.get(pk=sale_item)
    actions.generate_movement_stock_item(instance=instance)
