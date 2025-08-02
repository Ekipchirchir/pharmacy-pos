from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('sales/', views.sales_view, name='sales'),
    path('suppliers/', views.suppliers_view, name='suppliers'),
    path('reports/', views.reports_view, name='reports'),
    path('settings/', views.settings_view, name='settings'),
]