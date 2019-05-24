from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

from core import actions, models


@shared_task(queue='stock')
def generate_movement_stock(sale: int):
    instance = models.Sale.objects.get(pk=sale)
    actions.generate_movement_stock(instance=instance)


@shared_task(queue='stock')
def generate_movement_stock_item(sale_item: int):
    instance = models.SaleItem.objects.get(pk=sale_item)
    actions.generate_movement_stock_item(instance=instance)


MINUTES = "00, 10, 20, 30, 40, 50"


@periodic_task(
    run_every=(crontab(hour="*", minute=MINUTES, day_of_week="*")),
    options={'queue': 'stock'}
)
def test():
    pass
