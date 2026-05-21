from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import OrderSerializer
from accounts.permissions import IsAdmin
from django.db.models import Count, Sum
from rest_framework.pagination import PageNumberPagination

# GET ALL ORDERS
class OrderPagination(PageNumberPagination):

    page_size = 5
    page_size_query_param = 'page_size'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):

    search = request.GET.get('search')

    status_filter = request.GET.get('status')

    orders = Order.objects.all().order_by('-created_at')

    if search:
        orders = orders.filter(customer_name__icontains=search)

    if status_filter:
        orders = orders.filter(status=status_filter)

    paginator = OrderPagination()

    paginated_orders = paginator.paginate_queryset(
        orders,
        request
    )

    serializer = OrderSerializer(
        paginated_orders,
        many=True
    )

    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):

    total_orders = Order.objects.count()

    submitted_orders = Order.objects.filter(
        status='Submitted'
    ).count()

    approved_orders = Order.objects.filter(
        status='Approved'
    ).count()

    completed_orders = Order.objects.filter(
        status='Completed'
    ).count()

    total_revenue = Order.objects.aggregate(
        Sum('amount')
    )['amount__sum']

    data = {

        "total_orders": total_orders,

        "submitted_orders": submitted_orders,

        "approved_orders": approved_orders,

        "completed_orders": completed_orders,

        "total_revenue": total_revenue
    }

    return Response(data)


# CREATE ORDER
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_order(request):

    if request.method == 'GET':
        return Response({
            "message": "Send POST request to create order"
        })

    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET SINGLE ORDER
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_order(request, pk):

    try:
        order = Order.objects.get(id=pk)

    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = OrderSerializer(order)

    return Response(serializer.data)


# UPDATE ORDER
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order(request, pk):

    try:
        order = Order.objects.get(id=pk)

    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = OrderSerializer(order, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE ORDER
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdmin])
def delete_order(request, pk):

    try:
        order = Order.objects.get(id=pk)

    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    order.delete()

    return Response({
        "message": "Order deleted successfully"
    })
