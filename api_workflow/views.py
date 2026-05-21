from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import OrderSerializer


# GET ALL ORDERS
@api_view(['GET'])
def get_orders(request):

    orders = Order.objects.all().order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)


# CREATE ORDER
@api_view(['GET', 'POST'])
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
