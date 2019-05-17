from itertools import chain

from django.db.models import OuterRef, Subquery, Sum, FloatField, Case, When, Q, CharField, Count, Value, \
    ExpressionWrapper, F, Avg

from core import models


def query9():
    subquery = models.Employee.objects.annotate(
        sum_salary=Sum('salary')
    ).filter(
        departament=OuterRef('pk')
    )
    subquery.query.group_by = None
    queryset = models.Departament.objects.annotate(
        total=Subquery(subquery.values('sum_salary'), output_field=FloatField())
    )
    return queryset.values('name', 'total')


def query10():
    queryset = models.Customer.objects.annotate(
        _gender=Case(
            When(condition=Q(gender=models.Customer.FEMALE), then=Value('FEMININO')),
            default=Value('MASCULINO'),
            output_field=CharField()
        )
    ).values('_gender').annotate(
        count_gender=Count('*')
    ).values('_gender', 'count_gender')
    return queryset


def query11(year: int = 2011):
    subquery = models.SaleItem.objects.select_related('product', 'sale').annotate(
        subtotal=Sum(ExpressionWrapper(
            F('quantity') * F('product__sale_price'), output_field=FloatField()
        ), output_field=FloatField())
    ).filter(
        product__product_group=OuterRef('id'),
        sale__date__year=year
    )
    subquery.query.group_by = None
    queryset = models.ProductGroup.objects.annotate(
        sale_total=Subquery(subquery.values('subtotal'), output_field=FloatField())
    ).values(
        'description', 'sale_total'
    )
    return queryset


def query12():
    models.SaleItem.objects.select_related('product', 'product__product_group').values(
        'product__product_group__description'
    ).annotate(
        sale_total=Sum(ExpressionWrapper(
            F('quantity') * F('product__sale_price'), output_field=FloatField()
        ), output_field=FloatField())
    ).values('product__product_group__description', 'sale_total')


def gain_by_product_group(year: int):
    return models.SaleItem.objects.select_related('sale', 'product', 'product__product_group').annotate(
        subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField())
    ).filter(sale__date__year=year).values('product__product_group__description').annotate(
        gain=Sum(ExpressionWrapper(
            F('subtotal') * F('product__product_group__gain_percentage') / Value(100), output_field=FloatField()
        ), output_field=FloatField())
    ).values('product__product_group__description', 'gain')


def total_customer_by_marital_status():
    return models.Customer.objects.select_related('marital_status').values(
        'marital_status__description'
    ).annotate(counter=Count('id')).values('marital_status__description', 'counter')


def total_customer_by_zone():
    return models.Customer.objects.select_related('district', 'district__zone').values(
        'district__zone__name'
    ).annotate(counter=Count('id')).values('district__zone__name', 'counter')
