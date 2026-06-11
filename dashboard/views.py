from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from sales.models import SalesOrder
from customers.models import Customer
from products.models import Product


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user

    def _is_admin(u):
        return (
            u.is_superuser
            or u.groups.filter(name__in=['Admin', 'Sales Head']).exists()
            or getattr(getattr(u, 'profile', None), 'role', '') in ('admin', 'manager')
        )

    is_admin = _is_admin(user)

    if is_admin:
        orders_qs = SalesOrder.objects.all()
        customers_qs = Customer.objects.all()
    else:
        orders_qs = SalesOrder.objects.filter(sales_rep=user)
        customers_qs = Customer.objects.filter(created_by=user)

    products_qs = Product.objects.all()

    today = timezone.now().date()
    month_start = today.replace(day=1)
    yesterday = today - timedelta(days=1)

    total_revenue = orders_qs.filter(status='Completed').aggregate(
        s=Sum('total_amount')
    )['s'] or 0

    monthly_revenue = orders_qs.filter(
        status='Completed',
        created_at__date__gte=month_start
    ).aggregate(s=Sum('total_amount'))['s'] or 0

    today_sales = orders_qs.filter(
        created_at__date=today
    ).aggregate(s=Sum('total_amount'))['s'] or 0

    yesterday_sales = orders_qs.filter(
        created_at__date=yesterday
    ).aggregate(s=Sum('total_amount'))['s'] or 0

    today_change = 0
    if yesterday_sales:
        today_change = round(((today_sales - yesterday_sales) / yesterday_sales) * 100, 1)

    pending_count = orders_qs.filter(status='Pending').count()
    approved_count = orders_qs.filter(status='Approved').count()
    processing_count = orders_qs.filter(status='Processing').count()
    completed_count = orders_qs.filter(status='Completed').count()
    total_orders = orders_qs.count()

    total_stock = products_qs.aggregate(s=Sum('stock'))['s'] or 0
    total_stock_value = sum(
        p.stock * p.unit_price for p in products_qs
    )

    # Monthly breakdown (last 12 months)
    monthly_data = []
    for i in range(11, -1, -1):
        d = today.replace(day=1) - timedelta(days=i * 28)
        m_start = d.replace(day=1)
        if m_start.month == 12:
            m_end = m_start.replace(year=m_start.year + 1, month=1, day=1)
        else:
            m_end = m_start.replace(month=m_start.month + 1, day=1)
        rev = orders_qs.filter(
            created_at__date__gte=m_start,
            created_at__date__lt=m_end,
        ).aggregate(s=Sum('total_amount'))['s'] or 0
        cnt = orders_qs.filter(
            created_at__date__gte=m_start,
            created_at__date__lt=m_end,
        ).count()
        monthly_data.append({
            'month': m_start.strftime('%b'),
            'revenue': float(rev),
            'orders': cnt,
        })

    return Response({
        'total_revenue': float(total_revenue),
        'monthly_revenue': float(monthly_revenue),
        'today_sales': float(today_sales),
        'today_change': today_change,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'processing_count': processing_count,
        'completed_count': completed_count,
        'total_orders': total_orders,
        'total_customers': customers_qs.count(),
        'total_stock': total_stock,
        'total_stock_value': float(total_stock_value),
        'monthly_data': monthly_data,
    })
