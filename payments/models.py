from email.policy import default
from django.db import models
from uuid import uuid4
from django.utils import timezone


class PaymentTransaction(models.Model):
    status_choices = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )

    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='payment_transactions')

    amount = models.IntegerField()

    status = models.CharField(max_length=255, choices=status_choices, default='PENDING')

    created_at = models.DateTimeField(default=timezone.localtime)
    updated_at = models.DateTimeField(null=True, blank=True)


class StripeTransaction(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    payment_transaction = models.OneToOneField(PaymentTransaction, on_delete=models.CASCADE, related_name='stripe_transaction')

    stripe_transaction_id = models.CharField(max_length=255, null=True, blank=True)

    paid = models.BooleanField(default=False)

    invoice_dump = models.JSONField(default=dict)
    
    payment_link = models.URLField(null=True, blank=True)

    hook_dump = models.JSONField(default=dict)

    def price(self):
        return self.payment_transaction.amount
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.paid:
            self.payment_transaction.status = 'COMPLETED'
            self.payment_transaction.save()
