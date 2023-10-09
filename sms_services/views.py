from django.shortcuts import render, redirect
import requests
from django.db.models import Q
from django.http import QueryDict

from datetime import datetime, timezone

from .models import Outbox, DeliveryReport


from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import Outboxform
from django.views.decorators.csrf import csrf_exempt
from transactions.models import Transaction
from django.http import HttpResponse
from django.core.paginator import Paginator


def outboxhome(request):
    template_name = "sms_services/outbox.html"
    messages = Outbox.objects.all()
    paginated_messages = Paginator(messages, 12)
    page_number = request.GET.get("page")
    messages = paginated_messages.get_page(page_number)

    context = {
        "messages": messages,
    }
    return render(request, template_name, context)


def deliveryreport(request):
    template_name = "sms_services/delivery-reports.html"
    reports = DeliveryReport.objects.all()

    paginated_reports = Paginator(reports, 20)
    page_number = request.GET.get("page")
    reports = paginated_reports.get_page(page_number)
    context = {"reports": reports}
    return render(request, template_name, context)


def create_sms(request):
    form = Outboxform(request.user)
    if request.method == "POST":
        form = Outboxform(request.user, request.POST)
        if form.is_valid():
            staff = request.user
            phone_numbers = form.cleaned_data.get("phone_numbers")
            text_message = form.cleaned_data.get("text_message")
            Outbox.send(phone_numbers, text_message)

            message = Outbox.objects.create(
                phone_numbers=phone_numbers, text_message=text_message, staff=staff
            )
            message.save()

            return redirect("messages")

    return render(request, "sms_services/create-message.html", {"form": form})


@csrf_exempt
def incoming_delivery_reports(request):
    phoneNumber = request.POST.get("phoneNumber")
    retryCount = request.POST.get("retryCount")
    status = request.POST.get("status")
    networkCode = request.POST.get("networkCode")
    identifier = request.POST.get("id")
    DeliveryReport_object = DeliveryReport(
        identifier=identifier,
        phoneNumber=phoneNumber,
        retryCount=retryCount,
        status=status,
        networkCode=networkCode,
    )
    DeliveryReport_object.save()
    return HttpResponse(status=200)
    # https://www.branchbusinessadvance.com/sms-services/delivery_reports


@login_required
def outbox_search(request):
    messages = Outbox.objects.all()
    search = request.GET.get("search")
    if search:
        messages = messages.filter(
            Q(phone_numbers__icontains=search)
            | Q(date__icontains=search)
            | Q(text_message__icontains=search)
        )

    context = {
        "messages": messages,
    }

    return render(request, "sms_services/partials/outbox-partial.html", context)


@login_required
def report_search(request):
    reports = DeliveryReport.objects.all()
    search = request.GET.get("search")
    if search:
        reports = reports.filter(
            Q(phoneNumber__icontains=search) | Q(status__icontains=search)
        )

    context = {
        "reports": reports,
    }

    return render(request, "sms_services/partials/reports-partial.html", context)


@login_required
def delete_sent_messages(request):
    data = request.body.decode("utf-8")
    messages = QueryDict(data, mutable=True)
    ids = messages.getlist("ids")
    Outbox.objects.filter(pk__in=ids).delete()
    messages = Outbox.objects.all()
    paginated_messages = Paginator(messages, 12)
    page_number = request.GET.get("page")
    messages = paginated_messages.get_page(page_number)
    context = {
        "messages": messages,
    }
    return render(request, "sms_services/outbox.html", context)


@login_required
def delete_message_reports(request):
    data = request.body.decode("utf-8")
    reports = QueryDict(data, mutable=True)

    ids = reports.getlist("ids")
    DeliveryReport.objects.filter(pk__in=ids).delete()
    reports = DeliveryReport.objects.all()
    paginated_reports = Paginator(reports, 20)
    page_number = request.GET.get("page")
    reports = paginated_reports.get_page(page_number)
    context = {"reports": reports}
    return render(request, "sms_services/delivery-reports.html", context)


# ======================================BULK SMS MESSAGES==================================


@login_required
def sms_overdue_loans(request):
    loans = Transaction.objects.filter(
        Q(status="overdue") & Q(loan_amount__isnull=False)
    )

    for loan in loans:
        PRO_API_KEY = "07a2157f1da57fc2ad5ae8feead39f0ad2ec8bc2a3111887aaa7a96a35683560"
        PRO_USERNAME = "kejapro"
        # FROM ='Manipap'
        url = "https://api.africastalking.com/version1/messaging"
        headers = {
            "ApiKey": PRO_API_KEY,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        body = {
            "username": PRO_USERNAME,
            #  'from':FROM,
            "message": f"Your loan of {loan.outstanding_loan} is overdue",
            "to": [loan.client.phone1],
        }
        requests.post(url=url, headers=headers, data=body)

    myfilter = Transaction.objects.filter(
        Q(status="approved") | Q(status="overdue") | Q(status="rolled over")
    )
    loans = myfilter.filter(loan_amount__isnull=False).select_related("staff", "client")
    paginated_loans = Paginator(loans, 20)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {"loans": loans}
    return render(request, "sms_services/partials/loans-partial.html", context)


@login_required
def sms_due_today(request):
    today = datetime.now(timezone.utc)
    loans = Transaction.objects.filter(Q(loan_amount__isnull=False))
    for loan in loans:
        if today != loan.due_date:
            PRO_API_KEY = (
                "07a2157f1da57fc2ad5ae8feead39f0ad2ec8bc2a3111887aaa7a96a35683560"
            )
            PRO_USERNAME = "kejapro"
            # FROM ='Manipap'
            url = "https://api.africastalking.com/version1/messaging"
            headers = {
                "ApiKey": PRO_API_KEY,
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            }

            body = {
                "username": PRO_USERNAME,
                #  'from':FROM,
                "message": f"Your loan of {loan.outstanding_loan} is due today",
                "to": [loan.client.phone1],
            }
            requests.post(url=url, headers=headers, data=body)

    loans = Transaction.objects.filter(
        ~Q(status="not approved")
        & ~Q(status="bad debt")
        & ~Q(status="cleared")
        & Q(loan_amount__isnull=False)
    ).select_related("staff", "client")
    paginated_loans = Paginator(loans, 20)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {"loans": loans}
    return render(request, "sms_services/partials/loans-partial.html", context)


#  send_mail('Kejapro verification code',message,'repotranscompany@gmail.com',[email],fail_silently=False)


@login_required
def email_all_clients(request):
    loans = Transaction.objects.filter(
        ~Q(status="not approved")
        & ~Q(status="bad debt")
        & ~Q(status="cleared")
        & Q(loan_amount__isnull=False)
    ).select_related("staff", "client")
    for loan in loans:
        send_mail(
            "Timeline digital ventures",
            f"Your outstanding loan of {loan.outstanding_loan} is due on {loan.due_date.date()}",
            "repotranscompany@gmail.com",
            [loan.client.email],
            fail_silently=False,
        )

    myfilter = Transaction.objects.filter(
        Q(status="approved") | Q(status="overdue") | Q(status="rolled over")
    )
    loans = myfilter.filter(loan_amount__isnull=False).select_related("staff", "client")
    paginated_loans = Paginator(loans, 20)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {"loans": loans}
    return render(request, "sms_services/partials/loans-partial.html", context)
