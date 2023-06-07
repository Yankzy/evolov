from django.contrib import admin
from . import models


class StripeTransactionAdmin(admin.ModelAdmin):
    list_display = 'price', 'paid'


admin.site.register(models.StripeTransaction, StripeTransactionAdmin)
admin.site.register(models.PaymentTransaction)