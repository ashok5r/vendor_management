from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from vendors.models import Vendor, PurchaseOrder

class VendorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a sample vendor for testing
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'Contact Details',
            'address': 'Vendor Address',
            'vendor_code': 'V123',
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_get_vendor_list(self):
        # Test retrieving the list of vendors
        url = reverse('vendor_list_create')  # Assuming 'vendor_list_create' is the correct URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure that the response contains one vendor

    def test_get_vendor_detail(self):
        # Test retrieving details of a specific vendor
        url = reverse('vendors:vendor_detail', args=[self.vendor.id])  # Assuming 'vendors:vendor_detail' is the correct URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor_data['name'])  # Ensure that the correct vendor details are returned

class PurchaseOrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a sample vendor and a purchase order for testing
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Contact Details',
            address='Address',
            vendor_code='V001',
        )
        self.po_data = {
            'po_number': 'P0001',
            'vendor': self.vendor,
            'order_date': timezone.now(),
            'delivery_date': timezone.now() + timezone.timedelta(days=7),
            'items': {'item1': 5, 'item2': 10},
            'quantity': 15,
            'status': 'pending',
            'issue_date': timezone.now(),
        }
        self.po = PurchaseOrder.objects.create(**self.po_data)

    def test_get_purchase_order_list(self):
        # Test retrieving the list of purchase orders
        url = reverse('vendors:purchase_order_list_create')  # Assuming 'vendors:purchase_order_list_create' is the correct URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure that the response contains one purchase order

    def test_get_purchase_order_detail(self):
        # Test retrieving details of a specific purchase order
        url = reverse('vendors:purchase_order_detail', args=[self.po.id])  # Assuming 'vendors:purchase_order_detail' is the correct URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.po_data['po_number'])  # Ensure that the correct purchase order details are returned