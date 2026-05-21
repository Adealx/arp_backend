from django.shortcuts import render, redirect
from .models import Customer
from .forms import CustomerForm
from django.shortcuts import render, redirect, get_object_or_404


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {
        'customers': customers
    })


def add_customer(request):
    form = CustomerForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('customer_list')

    return render(request, 'customers/add_customer.html', {
        'form': form
    })

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    return render(request, 'customers/customer_detail.html', {
        'customer': customer
    })

def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    form = CustomerForm(request.POST or None, instance=customer)

    if form.is_valid():
        form.save()
        return redirect('customer_detail', pk=customer.pk)

    return render(request, 'customers/update_customer.html', {
        'form': form
    })

def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')

    return render(request, 'customers/delete_customer.html', {
        'customer': customer
    })