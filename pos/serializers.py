from rest_framework import serializers
from .models import Drug, Sale, SaleItem

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['id', 'name', 'batch_number', 'quantity', 'price', 'expiry_date']

class SaleItemSerializer(serializers.ModelSerializer):
    drug = DrugSerializer(read_only=True)
    drug_id = serializers.PrimaryKeyRelatedField(queryset=Drug.objects.all(), source='drug')

    class Meta:
        model = SaleItem
        fields = ['id', 'drug', 'drug_id', 'quantity', 'subtotal']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Sale
        fields = ['id', 'invoice_id', 'total_amount', 'phone_number', 'created_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        for item_data in items_data:
            drug = item_data['drug']
            quantity = item_data['quantity']
            subtotal = drug.price * quantity
            SaleItem.objects.create(sale=sale, drug=drug, quantity=quantity, subtotal=subtotal)
            # Update drug inventory
            drug.quantity -= quantity
            drug.save()
        return sale