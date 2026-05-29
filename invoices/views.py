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


def dashboard(request):

    invoices = Invoice.objects.all()
    payments = Payment.objects.all()

    total_revenue = sum(p.amount_paid for p in payments)
    total_invoiced = sum(i.amount for i in invoices)

    outstanding = sum(i.balance_due for i in invoices)

    overdue_invoices = invoices.filter(
        due_date__lt=timezone.now().date(),
        status__in=['Pending', 'Partially Paid']
    ).count()

    context = {
        'total_revenue': total_revenue,
        'total_invoiced': total_invoiced,
        'outstanding': outstanding,
        'overdue_invoices': overdue_invoices,
        'total_invoices': invoices.count(),
        'total_payments': payments.count(),
    }

    return render(request, 'dashboard.html', context)

def invoice_list(request):
    invoices = Invoice.objects.all()

    return render(request, 'invoices/invoice_list.html', {
        'invoices': invoices
    })


def add_invoice(request):
    form = InvoiceForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('invoice_list')

    return render(request, 'invoices/add_invoice.html', {
        'form': form
    })

def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    return render(request, 'invoices/invoice_detail.html', {
        'invoice': invoice
    })

def update_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    form = InvoiceForm(request.POST or None, instance=invoice)

    if form.is_valid():
        form.save()
        return redirect('invoice_detail', pk=invoice.pk)

    return render(request, 'invoices/update_invoice.html', {
        'form': form
    })

def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')

    return render(request, 'invoices/delete_invoice.html', {
        'invoice': invoice
    })