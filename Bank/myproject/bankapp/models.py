from django.db import models

class Customer(models.Model):
    account_id = models.IntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    account = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()
    description = models.CharField(max_length=255)
    debit_credit_status = models.CharField(max_length=1, choices=[('D', 'Debit'), ('C', 'Credit')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.debit_credit_status == 'D':
            previous_balance = Transaction.objects.filter(account=self.account, transaction_date__lt=self.transaction_date).order_by('-transaction_date').first()
            if previous_balance:
                self.balance = previous_balance.balance + self.amount
            else:
                self.balance = self.amount
        else:
            previous_balance = Transaction.objects.filter(account=self.account, transaction_date__lt=self.transaction_date).order_by('-transaction_date').first()
            if previous_balance:
                self.balance = previous_balance.balance - self.amount
            else:
                self.balance = -self.amount

        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.account.name} - {self.description}"


class Point(models.Model):
    account = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_point = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.account.name} - Point: {self.total_point}"