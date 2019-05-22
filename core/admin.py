from django.contrib import admin

# Register your models here.
from core import models


@admin.register(models.StockAddress)
class StockAddressModelAdmin(admin.ModelAdmin):
    pass


class SaleItemInLine(admin.TabularInline):
    model = models.SaleItem
    readonly_fields = ['subtotal']
    extra = 1


@admin.register(models.Sale)
class SaleModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'employee', 'customer')
    list_per_page = 10
    inlines = [SaleItemInLine]
