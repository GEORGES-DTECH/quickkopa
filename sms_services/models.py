import requests
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.db.models import Count, Sum
from django.urls import reverse


class Outbox(models.Model):
    date = models.DateTimeField(default=timezone.now)
    text_message = models.TextField(max_length=160, null=True, blank=True)
    phone_numbers = models.TextField(null=True, blank=True)
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ("-date",)
        verbose_name = "Outbox"
        verbose_name_plural = "Outbox"

    def get_absolute_url(self):
        return reverse("messages")

    @staticmethod
    def send(phone_numbers, text_message):
        PRO_API_KEY = "07a2157f1da57fc2ad5ae8feead39f0ad2ec8bc2a3111887aaa7a96a35683560"

        PRO_USERNAME = "kejapro"
        # FROM ="Kejapro"

        url = "https://api.africastalking.com/version1/messaging"
        headers = {
            "ApiKey": PRO_API_KEY,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        body = {
            "username": PRO_USERNAME,
            "message": text_message,
            # 'from':FROM,
            "to": [phone_numbers],
        }
        response = requests.post(url=url, headers=headers, data=body)
        return response


class DeliveryReport(models.Model):
    identifier = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    phoneNumber = models.CharField(max_length=15, blank=True, null=True)
    retryCount = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    networkCode = models.IntegerField(blank=True, null=True)
    top_up = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ("-date",)
        verbose_name = "Delivery Report"
        verbose_name_plural = "Delivery Reports"

    @cached_property
    def total_sms(self):
        return DeliveryReport.objects.filter(status="success").count()

    @cached_property
    def total_top_up(self):
        result = DeliveryReport.objects.aggregate(total=Sum("top_up"))
        return result["total"]

    @cached_property
    def cost_of_messages(self):
        method = self.total_sms
        cost_per_sms = 0.8
        return method * cost_per_sms

    @cached_property
    def wallet_balance(self):
        method = self.total_top_up
        method2 = self.cost_of_messages
        if method2 is None:
            return 0
        if method is None:
            return 0
        return method - method2
