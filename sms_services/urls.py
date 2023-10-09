from django.urls import path
from .views import (
    outboxhome,
    create_sms,
    delete_sent_messages,
    incoming_delivery_reports,
    outbox_search,
    deliveryreport,
    report_search,
    delete_message_reports,
    delete_sent_messages,
    sms_overdue_loans,
    sms_due_today,
    email_all_clients,
)

urlpatterns = [
    path("create-message", create_sms, name="create-message"),
    path("messages", outboxhome, name="messages"),
    path("reports", deliveryreport, name="reports-home"),
    path("email-clients", email_all_clients, name="email-clients"),
    path("sms-overdue-loans", sms_overdue_loans, name="sms-overdue-loans"),
    path("sms-today-loans", sms_due_today, name="sms-due-today"),
    path("incoming-reports", incoming_delivery_reports, name="incoming-reports"),
    path("outbox-search", outbox_search, name="outbox-search"),
    path("report-search", report_search, name="report-search"),
    path("delete-messages", delete_sent_messages, name="delete-messages"),
    path(
        "delete-message-reports", delete_message_reports, name="delete-message-reports"
    ),
]
