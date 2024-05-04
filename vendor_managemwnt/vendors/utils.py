from django.db.models import Avg, Count
from django.utils import timezone
from .models import Vendor, PurchaseOrder, HistoricalPerformance

def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now())
    return (on_time_deliveries.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0

def calculate_quality_rating_avg(vendor):
    completed_pos_with_rating = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    return completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

def calculate_average_response_time(vendor):
    acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    response_times = (acknowledged_pos.values('acknowledgment_date') - acknowledged_pos.values('issue_date')).aggregate(Avg('acknowledgment_date'))['acknowledgment_date__avg']
    return response_times.total_seconds() if response_times else 0

def calculate_fulfillment_rate(vendor):
    issued_pos = PurchaseOrder.objects.filter(vendor=vendor)
    successful_fulfillments = issued_pos.filter(status='completed', issue_date__lte=timezone.now())
    return (successful_fulfillments.count() / issued_pos.count()) * 100 if issued_pos.count() > 0 else 0

def update_vendor_performance_metrics(vendor):
    vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
    vendor.quality_rating_avg = calculate_quality_rating_avg(vendor)
    vendor.average_response_time = calculate_average_response_time(vendor)
    vendor.fulfillment_rate = calculate_fulfillment_rate(vendor)
    vendor.save()

def update_historical_performance(vendor):
    HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=calculate_on_time_delivery_rate(vendor),
        quality_rating_avg=calculate_quality_rating_avg(vendor),
        average_response_time=calculate_average_response_time(vendor),
        fulfillment_rate=calculate_fulfillment_rate(vendor),
    )