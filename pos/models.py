from django.db import models
from django.utils import timezone
from datetime import timedelta

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Drug(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    batch_number = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    manufacturing_date = models.DateField()
    category = models.CharField(max_length=50, choices=[('Tablet', 'Tablet'), ('Syrup', 'Syrup'), ('Injection', 'Injection')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Batch: {self.batch_number})"

    def is_near_expiry(self):
        three_months_from_now = timezone.now().date() + timedelta(days=90)
        return self.expiry_date <= three_months_from_now and self.quantity > 0

class Sale(models.Model):
    invoice_id = models.CharField(max_length=20, unique=True, default="INV" + str(timezone.now().timestamp()))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15, blank=True)  # For M-Pesa
    customer_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale {self.invoice_id} - KES {self.total_amount}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name="items", on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    prescription_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.drug.name} x {self.quantity}"