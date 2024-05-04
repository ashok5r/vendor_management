from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from .models import vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.utils import timezone
from .utils import update_vendor_performance_metrics



# Create your views here.

class VendorListCreateView(generics.ListCreateAPIView):
     
    #  API view to list all vendors or create a new vendor.
     
    queryset = vendor.objects.all()
    serializer_class = VendorSerializer

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
     
    # API view to retrieve, update, or delete a specific vendor.
     
    queryset = vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
     
    # API view to list all purchase orders or create a new purchase order.
     
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
     
    # API view to retrieve, update, or delete a specific purchase order.
     
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
     
    # API view to retrieve historical performance metrics of a vendor.
     
    queryset = vendor.objects.all()
    serializer_class = HistoricalPerformanceSerializer 

class PurchaseOrderAcknowledgeView(generics.UpdateAPIView):
     
    # API view to acknowledge a purchase order.
     
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, *args, **kwargs):
        
        # Custom action to acknowledge a purchase order and update vendor performance metrics.
         
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        update_vendor_performance_metrics(purchase_order.vendor)  # Update vendor performance metrics
        return Response({'status': 'Acknowledged successfully'})