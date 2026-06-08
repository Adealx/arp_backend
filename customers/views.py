from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.http import HttpResponseForbidden

from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import Response
from rest_framework import status

from .models import Customer
from .forms import CustomerForm
from .serializers import CustomerSerializer

from audit_logs.utils import create_audit_log


def customer_list(request):

    user = request.user

    if (
        user.is_superuser
        or user.groups.filter(
            name__in=['Admin', 'Sales Head']
        ).exists()
    ):
        customers = Customer.objects.all()

    else:
        customers = Customer.objects.filter(
            created_by=user
        )

    return render(
        request,
        'customers/customer_list.html',
        {'customers': customers}
    )


def add_customer(request):

    form = CustomerForm(request.POST or None)

    if form.is_valid():

        customer = form.save(commit=False)

        customer.created_by = request.user

        customer.save()

        create_audit_log(
            request.user,
            'CREATE',
            'Customer',
            f'Created customer {customer.name}'
        )

        return redirect('customer_list')

    return render(
        request,
        'customers/add_customer.html',
        {'form': form}
    )


def customer_detail(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    if (
        customer.created_by != request.user
        and not request.user.is_superuser
        and not request.user.groups.filter(
            name__in=['Admin', 'Sales Head']
        ).exists()
    ):
        return HttpResponseForbidden(
            "You do not have permission to view this customer."
        )

    return render(
        request,
        'customers/customer_detail.html',
        {'customer': customer}
    )


def update_customer(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    if (
        customer.created_by != request.user
        and not request.user.is_superuser
        and not request.user.groups.filter(
            name__in=['Admin', 'Sales Head']
        ).exists()
    ):
        return HttpResponseForbidden(
            "You do not have permission to edit this customer."
        )

    form = CustomerForm(
        request.POST or None,
        instance=customer
    )

    if form.is_valid():

        form.save()

        return redirect(
            'customer_detail',
            pk=customer.pk
        )

    return render(
        request,
        'customers/update_customer.html',
        {'form': form}
    )


def delete_customer(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    if (
        customer.created_by != request.user
        and not request.user.is_superuser
        and not request.user.groups.filter(
            name__in=['Admin', 'Sales Head']
        ).exists()
    ):
        return HttpResponseForbidden(
            "You do not have permission to delete this customer."
        )

    if request.method == 'POST':

        customer.delete()

        return redirect('customer_list')

    return render(
        request,
        'customers/delete_customer.html',
        {'customer': customer}
    )


# ==========================
# API ENDPOINTS
# ==========================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def customer_api(request):

    user = request.user

    if request.method == 'GET':

        if user.profile.role in [
            'admin',
            'manager'
        ]:

            customers = Customer.objects.all()

        else:

            customers = Customer.objects.filter(
                created_by=user
            )

        serializer = CustomerSerializer(
            customers,
            many=True
        )

        return Response(
            serializer.data
        )

    serializer = CustomerSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save(
            created_by=request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_detail_api(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    user = request.user

    if (
        customer.created_by != user
        and user.profile.role not in [
            'admin',
            'manager'
        ]
    ):

        return Response(
            {
                "error": "Permission denied"
            },
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = CustomerSerializer(
        customer
    )

    return Response(
        serializer.data
    )