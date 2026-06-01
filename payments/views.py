from django.shortcuts import render, redirect
from .forms import PaymentForm


from django.http import HttpResponseForbidden


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

            return redirect('invoice_list')

    else:
        form = PaymentForm()

    return render(
        request,
        'payments/create_payment.html',
        {'form': form}
    )
