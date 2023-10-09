from django.db.models.signals import post_save
from django.core.cache import cache

from django.dispatch import receiver
from django.db.models import Q
from .models import Transaction, Payment



@receiver([post_save], sender=Payment)
def update_transactions(instance,*args,**kwargs):
    if instance.transaction is not None:
        loan = Transaction.objects.get(pk=instance.transaction.id)
        loan.save()

    if instance.transaction is None:
        loans = Transaction.objects.filter(
            ~Q(status="not approved")
            & ~Q(status="bad debt")
            & ~Q(status="cleared")
            & Q(loan_amount__isnull=False)
        ).select_related("staff","client")

        payments = Payment.objects.filter(transaction_id__isnull=True).select_related(
            "staff", "transaction__client","transaction__staff"
        )
        for loan in loans:
            for payment in payments:
                if loan.client.id_number == payment.BillRefNumber:
                    payment.transaction_id = loan.id
                    loan.save()
                    payment.save()
