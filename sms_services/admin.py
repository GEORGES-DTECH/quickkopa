from .models import Outbox, DeliveryReport
from django.contrib import admin


class Outboxadmin(admin.ModelAdmin):

    list_display = (
        "date",
        "phone_numbers",
        "text_message",
    )
    search_fields = (
        "date",
        "phone_numbers",
        "text_message",
    )
    list_per_page = 80
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class DeliveryReportadmin(admin.ModelAdmin):

    list_display = (
        "date",
        "phoneNumber",
        "status",
    )
    search_fields = (
        "date",
        "phoneNumber",
        "status",
    )
    list_per_page = 80
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Outbox, Outboxadmin)
admin.site.register(DeliveryReport, DeliveryReportadmin)
