from django.urls import path
from .views import (
    VendorListCreateView,
    VendorDetailView,
    PurchaseOrderListCreateView,
    PurchaseOrderDetailView,
    VendorPerformanceView,
)

app_name = 'vendors'  # Namespace for the app

urlpatterns = [
    # Vendor Profile Management Endpoints
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor_list_create'),  # List and create vendors
    path('api/vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor_detail'),  # Retrieve, update, or delete a specific vendor

    # Purchase Order Tracking Endpoints
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase_order_list_create'),  # List and create purchase orders
    path('api/purchase_orders/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchase_order_detail'),  # Retrieve, update, or delete a specific purchase order

    # Vendor Performance Evaluation Endpoints
    path('api/vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor_performance'),  # Retrieve historical performance metrics of a vendor
]