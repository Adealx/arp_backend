from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import Invoice
from .forms import InvoiceForm
from django.shortcuts import render
from .models import Invoice
from payments.models import Payment
from django.utils import timezone
from django.http import HttpResponseForbidden

from sales.models import SalesOrder
from customers.models import Customer


def dashboard(request):

    user = request.user

    # Admin, Sales Head, Super Admin
    if (
        user.is_superuser
        or user.groups.filter(
            name__in=['Admin', 'Sales Head']
        ).exists()
    ):

        invoices = Invoice.objects.all()
        payments = Payment.objects.all()
        customers = Customer.objects.all()
        sales_orders = SalesOrder.objects.all()

    # Sales Rep
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
        p.amount_paid
        for p in payments
    )

    total_invoiced = sum(
        i.amount
        for i in invoices
    )

    outstanding = sum(
        i.balance_due
        for i in invoices
    )

    overdue_invoices = invoices.filter(
        due_date__lt=timezone.now().date(),
        status__in=[
            'Pending',
            'Partially Paid'
        ]
    ).count()

    context = {

        'total_revenue': total_revenue,

        'total_invoiced': total_invoiced,

        'outstanding': outstanding,

        'overdue_invoices': overdue_invoices,

        'total_invoices': invoices.count(),

        'total_payments': payments.count(),

        'total_customers': customers.count(),

        'total_sales_orders': sales_orders.count(),
    }

    return render(
        request,
        'dashboard.html',
        context
    )

def invoice_list(request):

    user = request.user

    if (
        user.is_superuser
        or user.groups.filter(
            name__in=['Admin', 'Sales Head']
        ).exists()
    ):
        invoices = Invoice.objects.all()

    else:
        invoices = Invoice.objects.filter(
            created_by=user
        )

    return render(
        request,
        'invoices/invoice_list.html',
        {'invoices': invoices}
    )


def add_invoice(request):
    form = InvoiceForm(request.POST or None)

    if form.is_valid():
        invoice = form.save(commit=False)

        invoice.created_by = request.user

        invoice.save()

        return redirect('invoice_list')

    return render(
        request,
        'invoices/add_invoice.html',
        {'form': form}
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
            name__in=['Admin', 'Sales Head']
        ).exists()
    ):
        return HttpResponseForbidden(
            "You do not have permission to view this invoice."
        )

    return render(
        request,
        'invoices/invoice_detail.html',
        {'invoice': invoice}
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
            name__in=['Admin', 'Sales Head']
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
            'invoice_detail',
            pk=invoice.pk
        )

    return render(
        request,
        'invoices/update_invoice.html',
        {'form': form}
    )

def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')

    return render(request, 'invoices/delete_invoice.html', {
        'invoice': invoice
    })