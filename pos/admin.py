from django.contrib import admin
from .models import Drug, Sale, SaleItem, Supplier

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'batch_number', 'quantity', 'price', 'expiry_date', 'category')
    list_filter = ('expiry_date', 'category', 'supplier')
    search_fields = ('name', 'batch_number')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'total_amount', 'phone_number', 'customer_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('invoice_id', 'customer_name')

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'drug', 'quantity', 'subtotal', 'prescription_number')
    list_filter = ('sale', 'drug')
    search_fields = ('drug__name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'address')
    search_fields = ('name', 'contact_person', 'phone')