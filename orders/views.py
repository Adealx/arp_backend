from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):

    if request.user.profile.role in [
        "admin",
        "manager"
    ]:

        orders = Order.objects.all()

    else:

        orders = Order.objects.filter(
            created_by=request.user
        )

    data = []

    for order in orders:

        data.append({
            "id": order.id,
            "order_number": order.order_number,
            "amount": str(order.amount),
            "customer": order.customer.name,
        })

    return Response(data)