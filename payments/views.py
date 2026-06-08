from django.shortcuts import render, redirect
from .forms import PaymentForm


from django.http import HttpResponseForbidden
from audit_logs.utils import create_audit_log

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Payment
from .serializers import PaymentSerializer


def create_payment(request):

    user = request.user

    allowed_roles = [
        'Accounts Officer',
        'Finance Manager',
        'Admin'
    ]

    if (
        not user.is_superuser
        and not user.groups.filter(
            name__in=allowed_roles
        ).exists()
    ):
        return HttpResponseForbidden(
            "You do not have permission to record payments."
        )

    if request.method == 'POST':

        form = PaymentForm(request.POST)

        if form.is_valid():

            payment = form.save(commit=False)

            payment.created_by = request.user

            payment.save()

            create_audit_log(
                request.user,
                'CREATE',
                'Payment',
                f'Recorded payment of ₦{payment.amount_paid}'
            )

            return redirect('invoice_list')

    else:
        form = PaymentForm()

    return render(
        request,
        'payments/create_payment.html',
        {'form': form}
    )

@api_view(['GET', 'POST'])
def payment_api(request):

    if request.method == 'GET':

        payments = Payment.objects.all()

        serializer = PaymentSerializer(
            payments,
            many=True
        )

        return Response(serializer.data)

    if request.method == 'POST':

        serializer = PaymentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )