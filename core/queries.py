from django.db.models import Q, Value, CharField, ExpressionWrapper, F, DecimalField
from django.db.models.functions import Upper, Lower, LPad, Cast

from core import models as core_models


def query1():
    q1 = core_models.Product.objects.all()
    q2 = core_models.Product.objects.filter(name__startswith='a')
    q3 = core_models.Product.objects.order_by('-id')
    q4 = core_models.Product.objects.values('id', 'name')
    q5 = core_models.Product.objects.get(pk=5)
    q6 = core_models.Product.objects.order_by('-id').first()
    q7 = core_models.Product.objects.order_by('id').last()
    q8 = core_models.Product.objects.exists()
    q9 = core_models.Product.objects.count()
    q10 = core_models.Product.objects.filter(Q(id__gt=4) | Q(name__startswith='a'))
    return q1, q2, q3, q4, q5, q6, q7, q8, q9


def query2():
    return core_models.Product.objects.values('name', 'product_group__description')


def query3():
    query = core_models.ProductGroup.objects.filter(description__in=['Limpeza', 'Bebidas'])
    return core_models.Product.objects.filter(product_group__in=query)


def query4():
    return core_models.Product.objects.filter(product_group__description__in=['Limpeza', 'Bebidas'])


def query5():
    return core_models.Product.objects.annotate(
        code=LPad(
            Cast('id', output_field=CharField()),
            6,
            Value('0')
        ),
        name_upper=Upper('name'),
        name_lower=Lower('name')
    ).values('code', 'name_upper', 'name_lower')


def query6():
    return core_models.Product.objects.annotate(
        custom_code=LPad(
            Cast('id', output_field=CharField()),
            6,
            Value('0')
        ),
    ).annotate(
        gain_price=ExpressionWrapper(
            F('sale_price') - F('cost_price'),
            output_field=DecimalField()
        )
    ).values('custom_code', 'name', 'gain_price')


def query7():
    return core_models.SaleItem.objects.annotate(
        custom_code=LPad(
            Cast('id', output_field=CharField()),
            6,
            Value('0')
        ),
        subtotal=ExpressionWrapper(
            F('quantity') * F('product__sale_price'),
            output_field=DecimalField()
        )
    ).order_by('product__name').values(
        'custom_code',
        'product__name',
        'quantity',
        'product__sale_price',
        'subtotal'
    )
