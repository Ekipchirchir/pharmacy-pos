from django.shortcuts import render
from django.contrib import messages
from .models import Drug, Sale, SaleItem, Supplier
from django.http import JsonResponse
import json
from django.db.models import ExpressionWrapper, DateField
from django.utils import timezone
from datetime import timedelta

def dashboard(request):
    total_drugs = Drug.objects.count()
    low_stock = Drug.objects.filter(quantity__lt=10).count()
    near_expiry = Drug.objects.filter(expiry_date__lte=timezone.now().date() + timedelta(days=90), quantity__gt=0).count()
    total_sales = Sale.objects.count()
    total_suppliers = Supplier.objects.count()
    # Get recent sales (last 7 days) for chart
    recent_sales = Sale.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)).order_by('created_at')
    sales_data = {
        'labels': [sale.created_at.strftime('%Y-%m-%d') for sale in recent_sales],
        'data': [float(sale.total_amount) for sale in recent_sales]
    }
    recent_sales_list = recent_sales[:5]  # Top 5 recent sales for table
    context = {
        'total_drugs': total_drugs,
        'low_stock': low_stock,
        'near_expiry': near_expiry,
        'total_sales': total_sales,
        'total_suppliers': total_suppliers,
        'sales_data': sales_data,
        'recent_sales': recent_sales_list
    }
    return render(request, 'dashboard.html', context)

# Rest of the views remain unchanged
def inventory_view(request):
    drugs = Drug.objects.all()
    expiry_alerts = Drug.objects.filter(expiry_date__lte=timezone.now().date() + timedelta(days=90), quantity__gt=0)
    context = {'drugs': drugs, 'expiry_alerts': expiry_alerts}
    return render(request, 'inventory.html', context)

def sales_view(request):
    drugs = Drug.objects.all()
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
            phone_number = data.get('phone_number', '')
            customer_name = data.get('customer_name', '')
            total_amount = sum(item['subtotal'] for item in items)
            sale = Sale.objects.create(total_amount=total_amount, phone_number=phone_number, customer_name=customer_name)
            for item_data in items:
                drug = Drug.objects.get(id=item_data['drug_id'])
                quantity = item_data['quantity']
                subtotal = drug.price * quantity
                SaleItem.objects.create(sale=sale, drug=drug, quantity=quantity, subtotal=subtotal, prescription_number=item_data.get('prescription_number', ''))
                drug.quantity -= quantity
                drug.save()
            messages.success(request, 'Sale processed successfully!')
            return JsonResponse({'message': 'Sale processed', 'invoice_id': sale.invoice_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    context = {'drugs': drugs}
    return render(request, 'sales.html', context)

def suppliers_view(request):
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        contact_person = request.POST.get('contact_person')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        Supplier.objects.create(name=name, contact_person=contact_person, phone=phone, email=email, address=address)
        messages.success(request, 'Supplier added successfully!')
        return redirect('suppliers')
    context = {'suppliers': suppliers}
    return render(request, 'suppliers.html', context)

def reports_view(request):
    sales = Sale.objects.all()
    context = {'sales': sales}
    return render(request, 'reports.html', context)

def settings_view(request):
    context = {}
    return render(request, 'settings.html', context)