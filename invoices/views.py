from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.http import HttpResponseForbidden
from django.utils import timezone

from rest_framework import status

from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Invoice
from .forms import InvoiceForm
from .serializers import InvoiceSerializer

from payments.models import Payment
from sales.models import SalesOrder
from customers.models import Customer
from audit_logs.utils import create_audit_log


def dashboard(request):

    user = request.user

    if (
        user.is_superuser
        or user.groups.filter(
            name__in=[
                "Admin",
                "Sales Head",
                "Accountant"
            ]
        ).exists()
    ):

        invoices = Invoice.objects.all()
        payments = Payment.objects.all()
        customers = Customer.objects.all()
        sales_orders = SalesOrder.objects.all()

    else:

        invoices = Invoice.objects.filter(
            created_by=user
        )

        customers = Customer.objects.filter(
            created_by=user
        )

        sales_orders = SalesOrder.objects.filter(
            sales_rep=user
        )

        payments = Payment.objects.filter(
            invoice__created_by=user
        )

    total_revenue = sum(
        payment.amount_paid
        for payment in payments
    )

    total_invoiced = sum(
        invoice.amount
        for invoice in invoices
    )

    outstanding = sum(
        invoice.balance_due
        for invoice in invoices
    )

    overdue_invoices = invoices.filter(
        due_date__lt=timezone.now().date(),
        status__in=[
            "Pending",
            "Partially Paid"
        ]
    ).count()

    context = {
        "total_revenue": total_revenue,
        "total_invoiced": total_invoiced,
        "outstanding": outstanding,
        "overdue_invoices": overdue_invoices,
        "total_invoices": invoices.count(),
        "total_payments": payments.count(),
        "total_customers": customers.count(),
        "total_sales_orders": sales_orders.count(),
    }

    return render(
        request,
        "dashboard.html",
        context
    )


def invoice_list(request):

    user = request.user

    if (
        user.is_superuser
        or user.groups.filter(
            name__in=[
                "Admin",
                "Sales Head",
                "Accountant"
            ]
        ).exists()
    ):

        invoices = Invoice.objects.all()

    else:

        invoices = Invoice.objects.filter(
            created_by=user
        )

    return render(
        request,
        "invoices/invoice_list.html",
        {
            "invoices": invoices
        }
    )


def add_invoice(request):

    form = InvoiceForm(
        request.POST or None
    )

    if form.is_valid():

        invoice = form.save(
            commit=False
        )

        invoice.created_by = request.user

        invoice.save()

        create_audit_log(
            request.user,
            "CREATE",
            "Invoice",
            f"Created invoice {invoice.invoice_number}"
        )

        return redirect(
            "invoice_list"
        )

    return render(
        request,
        "invoices/add_invoice.html",
        {
            "form": form
        }
    )


def invoice_detail(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk
    )

    if (
        invoice.created_by != request.user
        and not request.user.is_superuser
        and not request.user.groups.filter(
            name__in=[
                "Admin",
                "Sales Head",
                "Accountant"
            ]
        ).exists()
    ):

        return HttpResponseForbidden(
            "You do not have permission to view this invoice."
        )

    return render(
        request,
        "invoices/invoice_detail.html",
        {
            "invoice": invoice
        }
    )


def update_invoice(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk
    )

    if (
        invoice.created_by != request.user
        and not request.user.is_superuser
        and not request.user.groups.filter(
            name__in=[
                "Admin",
                "Sales Head",
                "Accountant"
            ]
        ).exists()
    ):

        return HttpResponseForbidden(
            "You do not have permission to edit this invoice."
        )

    form = InvoiceForm(
        request.POST or None,
        instance=invoice
    )

    if form.is_valid():

        form.save()

        return redirect(
            "invoice_detail",
            pk=invoice.pk
        )

    return render(
        request,
        "invoices/update_invoice.html",
        {
            "form": form
        }
    )


def delete_invoice(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk
    )

    if request.method == "POST":

        invoice.delete()

        return redirect(
            "invoice_list"
        )

    return render(
        request,
        "invoices/delete_invoice.html",
        {
            "invoice": invoice
        }
    )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def invoice_api(request):

    user = request.user

    if request.method == "GET":

        if user.profile.role in [
            "admin",
            "manager"
        ]:

            invoices = Invoice.objects.all()

        else:

            invoices = Invoice.objects.filter(
                created_by=user
            )

        serializer = InvoiceSerializer(
            invoices,
            many=True
        )

        return Response(
            serializer.data
        )

    serializer = InvoiceSerializer(
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def invoice_detail_api(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk
    )

    user = request.user

    if (
        invoice.created_by != user
        and user.profile.role not in [
            "admin",
            "manager"
        ]
    ):

        return Response(
            {
                "error": "Permission denied"
            },
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = InvoiceSerializer(
        invoice
    )

    return Response(
        serializer.data
    )


class InvoiceViewSet(ModelViewSet):

    serializer_class = InvoiceSerializer

    def get_queryset(self):

        user = self.request.user

        if user.profile.role in [
            "admin",
            "manager"
        ]:

            return Invoice.objects.all()

        return Invoice.objects.filter(
            created_by=user
        )

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )