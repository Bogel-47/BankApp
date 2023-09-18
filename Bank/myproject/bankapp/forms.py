from django import forms
from .models import Customer, Transaction
from django.forms.widgets import DateInput

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['account_id', 'name']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'transaction_date', 'description', 'debit_credit_status', 'amount']
        widgets = {
            'transaction_date': DateInput(attrs={'type': 'date'}),
        }
