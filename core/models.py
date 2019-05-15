from django.db import models
from django.utils.timezone import now


class ModelBase(models.Model):
    id = models.AutoField(
        db_column='id',
        null=False,
        primary_key=True
    )
    active = models.BooleanField(
        db_column='cs_active',
        null=False,
        default=True
    )
    created_at = models.DateTimeField(
        db_column='dt_created_at',
        null=False,
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        db_column='dt_modified_at',
        null=True,
        auto_now=True
    )

    class Meta:
        abstract = True


class Zone(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        null=False,
        max_length=54,
        unique=True
    )

    class Meta:
        db_table = 'zone'
        managed = True


class MeansPayment(ModelBase):
    description = models.CharField(
        db_column='tx_description',
        null=False,
        max_length=54,
        unique=True
    )

    class Meta:
        db_table = 'means_payment'
        managed = True


class State(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        null=False,
        max_length=54
    )
    abbreviation = models.CharField(
        db_column='tx_abbreviation',
        null=False,
        max_length=2
    )

    class Meta:
        db_table = 'state'
        managed = True


class City(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        null=False,
        max_length=54
    )
    state = models.ForeignKey(
        to='State',
        on_delete=models.DO_NOTHING,
        db_column='id_state',
        null=False,
        db_index=False
    )

    class Meta:
        db_table = 'city'
        managed = True
        indexes = [
            models.Index(fields=['state'])
        ]


class District(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        null=False,
        max_length=54
    )
    city = models.ForeignKey(
        to='City',
        on_delete=models.DO_NOTHING,
        db_column='id_city',
        null=False,
        db_index=False
    )
    zone = models.ForeignKey(
        to='Zone',
        on_delete=models.DO_NOTHING,
        db_column='id_zone',
        null=False,
        db_index=False
    )

    class Meta:
        db_table = 'district'
        managed = True
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['zone'])
        ]


class MaritalStatus(ModelBase):
    description = models.CharField(
        db_column='tx_description',
        null=False,
        max_length=54,
        unique=True
    )

    class Meta:
        db_table = 'marital_status'
        managed = True


class Customer(ModelBase):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )

    name = models.CharField(
        db_column='tx_name',
        null=False,
        max_length=104
    )
    salary = models.DecimalField(
        db_column='nb_salary',
        max_digits=10,
        decimal_places=4,
        null=False
    )
    gender = models.CharField(
        db_column='cs_gender',
        null=False,
        max_length=1,
        choices=GENDER_CHOICES
    )
    marital_status = models.ForeignKey(
        to='MaritalStatus',
        on_delete=models.DO_NOTHING,
        db_column='id_marital_status',
        null=False,
        db_index=False
    )
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False,
        db_index=False
    )

    class Meta:
        db_table = 'customer'
        managed = True
        indexes = [
            models.Index(fields=['marital_status']),
            models.Index(fields=['district'])
        ]


class BranchOffice(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        null=False,
        max_length=54,
        unique=True
    )
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False,
        db_index=False
    )

    class Meta:
        db_table = 'branch_office'
        managed = True
        indexes = [
            models.Index(fields=['district'])
        ]


class Supplier(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        null=False,
        max_length=54
    )
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False,
        db_index=False
    )

    class Meta:
        db_table = 'supplier'
        managed = True
        indexes = [
            models.Index(fields=['district'])
        ]


class Departament(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        null=False,
        max_length=54,
        unique=True
    )

    class Meta:
        db_table = 'departament'
        managed = True


class Employee(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        null=False,
        max_length=104
    )
    salary = models.DecimalField(
        db_column='nb_salary',
        max_digits=10,
        decimal_places=4,
        null=False
    )
    admission_date = models.DateField(
        db_column='dt_admission',
        null=False
    )
    date_birth = models.DateField(
        db_column='dt_birth',
        null=False
    )
    departament = models.ForeignKey(
        to='Departament',
        on_delete=models.DO_NOTHING,
        db_column='id_departament',
        null=False,
        db_index=False
    )
    marital_status = models.ForeignKey(
        to='MaritalStatus',
        on_delete=models.DO_NOTHING,
        db_column='id_marital_status',
        null=False,
        db_index=False
    )
    manager = models.ForeignKey(
        to='Employee',
        on_delete=models.DO_NOTHING,
        db_column='id_manager',
        null=True,
        db_index=False
    )

    class Meta:
        db_table = 'employee'
        managed = True
        indexes = [
            models.Index(fields=['departament']),
            models.Index(fields=['marital_status']),
            models.Index(fields=['manager']),
        ]


class ProductGroup(ModelBase):
    description = models.CharField(
        db_column='tx_description',
        null=False,
        max_length=54,
        unique=True
    )
    commission_percentage = models.DecimalField(
        db_column='nb_commission_percentage',
        max_digits=10,
        decimal_places=4,
        null=False
    )
    gain_percentage = models.DecimalField(
        db_column='nb_gain_percentage',
        max_digits=10,
        decimal_places=4,
        null=False
    )

    class Meta:
        db_table = 'product_group'
        managed = True


class Product(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        null=False,
        max_length=104
    )
    cost_price = models.DecimalField(
        db_column='nb_cost_price',
        max_digits=10,
        decimal_places=4,
        null=False
    )
    sale_price = models.DecimalField(
        db_column='nb_sale_price',
        max_digits=10,
        decimal_places=4,
        null=False
    )
    product_group = models.ForeignKey(
        to='ProductGroup',
        on_delete=models.DO_NOTHING,
        db_column='id_product_group',
        null=False,
        db_index=False
    )
    supplier = models.ForeignKey(
        to='Supplier',
        on_delete=models.DO_NOTHING,
        db_column='id_supplier',
        null=False,
        db_index=False
    )

    class Meta:
        db_table = 'product'
        managed = True
        indexes = [
            models.Index(fields=['product_group']),
            models.Index(fields=['supplier'])
        ]


class Sale(ModelBase):
    date = models.DateTimeField(
        db_column='dt_sale',
        null=False,
        default=now
    )
    employee = models.ForeignKey(
        to='Employee',
        on_delete=models.DO_NOTHING,
        db_column='id_employee',
        null=False,
        db_index=False
    )
    branch_office = models.ForeignKey(
        to='BranchOffice',
        on_delete=models.DO_NOTHING,
        db_column='id_branch_office',
        null=False,
        db_index=False
    )
    customer = models.ForeignKey(
        to='Customer',
        on_delete=models.DO_NOTHING,
        db_column='id_customer',
        null=False,
        db_index=False
    )

    class Meta:
        db_table = 'sale'
        managed = True
        indexes = [
            models.Index(fields=['employee']),
            models.Index(fields=['branch_office']),
            models.Index(fields=['customer'])
        ]


class SaleItem(ModelBase):
    sale = models.ForeignKey(
        to='Sale',
        on_delete=models.DO_NOTHING,
        db_column='id_sale',
        null=False,
        db_index=False
    )
    product = models.ForeignKey(
        to='Product',
        on_delete=models.DO_NOTHING,
        db_column='id_product',
        null=False,
        db_index=False
    )
    quantity = models.DecimalField(
        db_column='nb_quantity',
        max_digits=10,
        decimal_places=3,
        null=False
    )

    class Meta:
        db_table = 'sale_item'
        managed = True
        indexes = [
            models.Index(fields=['sale']),
            models.Index(fields=['product'])
        ]


class MeansPaymentSale(ModelBase):
    sale = models.ForeignKey(
        to='Sale',
        on_delete=models.DO_NOTHING,
        db_column='id_sale',
        null=False,
        db_index=False
    )
    means_payment = models.ForeignKey(
        to='MeansPayment',
        on_delete=models.DO_NOTHING,
        db_column='id_means_payment',
        null=False,
        db_index=False
    )
    value = models.DecimalField(
        db_column='nb_value',
        null=False,
        max_digits=16,
        decimal_places=4
    )

    class Meta:
        db_table = 'means_payment_sale'
        managed = True
        indexes = [
            models.Index(fields=['sale']),
            models.Index(fields=['means_payment']),
        ]
