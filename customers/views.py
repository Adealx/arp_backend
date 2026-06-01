from django.shortcuts import render, redirect
from .models import Customer
from .forms import CustomerForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden


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