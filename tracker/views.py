from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from django.db import models
from collections import defaultdict
import json

from .models import Transaction
from .forms import TransactionForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()

    # Get user transactions
    transactions = Transaction.objects.filter(user=user).order_by('-date')

    # Get date filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Summary
    income = transactions.filter(category='income').aggregate(models.Sum('amount'))['amount__sum'] or 0
    expenses = transactions.filter(category='expense').aggregate(models.Sum('amount'))['amount__sum'] or 0
    savings = income - expenses

    # Prepare data for chart
    daily_summary = defaultdict(lambda: {'income': 0, 'expense': 0})

    for txn in transactions:
        day = txn.date.strftime('%m-%d-%y')
        if txn.category in ['income', 'expense']:
            daily_summary[day][txn.category] += txn.amount

    sorted_dates = sorted(daily_summary.keys())
    labels = sorted_dates
    income_data = [daily_summary[day]['income'] for day in labels]
    expenses_data = [daily_summary[day]['expense'] for day in labels]

    return render(request, 'tracker/dashboard.html', {
        'transactions': transactions,
        'income': income,
        'expenses': expenses,
        'savings': savings,
        'labels': json.dumps(labels),
        'income_data': income_data,
        'expenses_data': expenses_data,
    })


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            txn = form.save(commit=False)
            txn.user = request.user
            txn.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'tracker/transaction_form.html', {'form': form, 'title': 'Add Transaction'})


@login_required
def update_transaction(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=txn)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=txn)
    return render(request, 'tracker/transaction_form.html', {'form': form, 'title': 'Update Transaction'})


@login_required
def delete_transaction(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        txn.delete()
        return redirect('dashboard')
    return render(request, 'tracker/delete_confirm.html', {'txn': txn})


def home_redirect(request):
    return redirect('login')