from django.shortcuts import render
from datetime import datetime
import calendar
# from django.views.decorators.cache import cache_page
from django.urls import reverse
from django.views import View
from django.core.cache import cache
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)

from .models import Transaction, Client, Payment
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from .forms import (
    Loancreationform,
    Loaneditform,
    Clientcreationform,
    Clientupdateform,
    Paymenteditform,
    Addpaymentform,
    Addexpenseform,
    Cashflowform,

)
from django.http import QueryDict
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator
from django_select2.views import AutoResponseView
from .serializers import Paymentserializer
from .filters import Annualfilter, Monthlyfilter


class Clientautocomplete(AutoResponseView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs[:3]


class Clientloanautocomplete(AutoResponseView):
    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(
            Q(status="approved")
            | Q(status="overdue")
            | Q(status="rolled over")
        )[:4]


class Staffautocomplete(AutoResponseView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_staff=True)


@login_required
def update_payments(request):
    update_payments = Payment.objects.filter(Q(amount__isnull=False)).select_related(
        "staff", "transaction__client", "transaction__staff"
    )[:1]
    payments = Payment.objects.filter(Q(TransAmount__isnull=False)).select_related(
        "staff", "transaction__client", "transaction__staff"
    )
    for payment in update_payments:
        payment.save()
    paginated_payments = Paginator(payments, 10)
    page_number = request.GET.get("page")
    payments = paginated_payments.get_page(page_number)
    context = {"payments": payments}
    cache.delete_many(["payments", "loans"])
    return render(request, "transactions/partials/payments-partial.html", context)


@login_required
def update_loans(request):
    loans = Transaction.objects.filter(
        ~Q(status="not approved")
       & ~Q(status="cleared")
        & Q(loan_amount__isnull=False)
    ).select_related("staff", "client")
    for loan in loans:
        loan.save()
    paginated_loans = Paginator(loans, 10)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {"loans": loans}
    cache.delete_many(["payments", "loans"])
    return render(request, "transactions/partials/loans-partial.html", context)


@login_required
def clear_loans(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Transaction.objects.filter(pk__in=checked_ids).update(status="cleared")
    loans = Transaction.objects.filter(
        ~Q(status="not approved")
      & ~Q(status="cleared")
        & Q(loan_amount__isnull=False)
    ).select_related("staff", "client")
    paginated_loans = Paginator(loans, 10)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {
        "loans": loans,
    }
    cache.delete("loans")
    return render(request, "transactions/partials/loans-partial.html", context)


@login_required
def approve_loans(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Transaction.objects.filter(pk__in=checked_ids).update(status="approved")

    loans = Transaction.objects.filter(
        ~Q(status="not approved")
       & ~Q(status="cleared")
        & Q(loan_amount__isnull=False)
    ).select_related("staff", "client")
    paginated_loans = Paginator(loans, 10)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {
        "loans": loans,
    }
    cache.delete("loans")
    return render(request, "transactions/partials/loans-partial.html", context)


@login_required
def rollover_loans(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Transaction.objects.filter(pk__in=checked_ids).update(status="rolled over")
    loans = Transaction.objects.filter(
        ~Q(status="not approved")
      & ~Q(status="cleared")
        & Q(loan_amount__isnull=False)
    ).select_related("staff", "client")
    paginated_loans = Paginator(loans, 10)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {
        "loans": loans,
    }
    cache.delete("loans")
    return render(request, "transactions/partials/loans-partial.html", context)


@login_required
def disapprove_loans(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Transaction.objects.filter(
        pk__in=checked_ids).update(status="not approved")
    loans = Transaction.objects.filter(
        ~Q(status="not approved")
      & ~Q(status="cleared")
        & Q(loan_amount__isnull=False)
    ).select_related("staff", "client")
    paginated_loans = Paginator(loans, 10)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {
        "loans": loans,
    }
    cache.delete("loans")
    return render(request, "transactions/partials/loans-partial.html", context)


@login_required
def reverse_loans(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Transaction.objects.filter(pk__in=checked_ids).update(status="approved")
    cache.delete("loans")
    cleared_loans = Transaction.objects.filter(loan_amount__isnull=False)
    loans = cleared_loans.filter(
        Q(status="cleared") | Q(status="bad debt") | Q(status="not approved")
    ).select_related("staff", "client")
    paginated_loans = Paginator(loans, 10)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {"loans": loans}
    return render(request, "transactions/partials/clearedloans-partial.html", context)



# =====================DETAIL VIEWS===========================

@login_required
def loan_history(request, pk):
    client = Client.objects.get(pk=pk)
    loans = client.transaction_set.filter(
        ~Q(status="not approved")
       
        & Q(loan_amount__isnull=False)
    ).select_related("staff", "client")
    context = {"loans": loans}
    return render(request, "transactions/detailviews/loan-history.html", context)


class Loandetail(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "transactions/detailviews/loan-detail.html"
    context_object_name = "loan"


class Clientdetail(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "transactions/detailviews/clients-detail.html"
    context_object_name = "client"


class Clientsdocuments(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "transactions/detailviews/clients-docs.html"
    context_object_name = "client"


@login_required
def loan_statement(request, pk):
    loan = Transaction.objects.get(pk=pk)
    payments = loan.payment_set.select_related("staff", "transaction", "transaction__client")
    context = {"payments": payments}
    return render(request, "transactions/detailviews/loan-statement.html", context)


class Staffreport(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "transactions/business-reports/staff-reports.html"
    context_object_name = "loan"


# ====================HOME VIEWS========================================


class Expenses(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/listviews/expenses.html"
        expenses = Transaction.objects.filter(
            expense_amount__isnull=False
        ).select_related("staff", "client")
        paginated_expenses = Paginator(expenses, 10)
        page_number = request.GET.get("page")
        expenses = paginated_expenses.get_page(page_number)
        context = {"expenses": expenses, "form": Addexpenseform()}
        return render(request, template_name, context)


class Cashflowtransactions(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/listviews/cashflow-transactions.html"
        transactions = Transaction.objects.filter(
            Q(transaction_amount__isnull=False)

        ).select_related("staff", "client")
        paginated_transactions = Paginator(transactions, 10)
        page_number = request.GET.get("page")
        transactions = paginated_transactions.get_page(page_number)
        context = {"transactions": transactions}
        return render(request, template_name, context)


class Paymentsview(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/listviews/payments.html"
        payments = cache.get("payments")
        if payments is None:
            payments = Payment.objects.filter(
                Q(TransAmount__isnull=False)
            ).select_related("staff", "transaction__client", "transaction__staff")
            cache.set("payments", payments)

        paginated_payments = Paginator(payments, 10)
        page_number = request.GET.get("page")
        payments = paginated_payments.get_page(page_number)
        context = {"payments": payments}
        return render(request, template_name, context)


class Loanview(LoginRequiredMixin, View):
    def get(self, request):
        if self.request.user.is_admin is True:
            template_name = "transactions/listviews/loans.html"
            loans = cache.get("loans")
            if loans is None:
                loans = Transaction.objects.filter(
                    ~Q(status="not approved")
                  & ~Q(status="cleared")
                    & Q(loan_amount__isnull=False)
                ).select_related("staff","client")
                cache.set("loans", loans)
            paginated_loans = Paginator(loans, 10)
            page_number = request.GET.get("page")
            loans = paginated_loans.get_page(page_number)
            context = {
                "loans": loans,
                "loan_form": Loancreationform(),
                "repayment": Addpaymentform(),

            }
            return render(request, template_name, context)
        if self.request.user.is_admin is False and self.request.user.is_staff is True:
            template_name = "transactions/listviews/staff-loans.html"
            loans = Transaction.objects.filter(
                ~Q(status="not approved")
               & ~Q(status="cleared")
                & Q(loan_amount__isnull=False)
                & Q(staff=self.request.user)
            ).select_related("staff", "client")
            paginated_loans = Paginator(loans, 20)
            page_number = request.GET.get("page")
            loans = paginated_loans.get_page(page_number)
            context = {
                "loans": loans,
            }
            return render(request, template_name, context)


class Overdueloansview(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/listviews/overdueloans.html"
        if self.request.user.is_admin is True:
            loans = Transaction.objects.filter(
                Q(loan_amount__isnull=False) & Q(status="overdue")
            ).select_related("staff", "client")
        if self.request.user.is_admin is False and self.request.user.is_staff is True:
            loans = Transaction.objects.filter(
                Q(loan_amount__isnull=False)
                & Q(status="overdue")
                & Q(staff=self.request.user)
            ).select_related("staff", "client")
        context = {
            "loans": loans,
        }
        return render(request, template_name, context)


class Monthlyloansduetoday(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/listviews/monthlyloans-due-today.html"
        self.date_today = datetime.now()
        today = f"{self.date_today.day}/{self.date_today.month}/{self.date_today.year}"
        myfilter = Transaction.objects.filter(
            ~Q(status="not approved")
           
            & ~Q(status="cleared")
            & Q(loan_amount__isnull=False)
        )
        if self.request.user.is_admin is True:
            loans = myfilter.filter(
                Q(day_month_year=today)
                & Q(payment_plan="monthly")
            ).select_related("staff", "client")
        if self.request.user.is_admin is False and self.request.user.is_staff is True:
            loans = myfilter.filter(

                Q(day_month_year=today)
                & Q(payment_plan="monthly")
                & Q(staff=self.request.user)
            ).select_related("staff", "client")
        context = {
            "loans": loans,
        }
        return render(request, template_name, context)


class Weeklyloansduetoday(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/listviews/weeklyloans-due-today.html"
        day_today = str(calendar.day_name[datetime.now().weekday()])
        myfilter = Transaction.objects.filter(
            ~Q(status="not approved")
        
            & ~Q(status="cleared")
            & Q(loan_amount__isnull=False)
        )
        if self.request.user.is_admin is True:
            loans = myfilter.filter(
               Q(day=day_today)
                & Q(payment_plan="weekly")
            ).select_related("staff", "client")
        if self.request.user.is_admin is False and self.request.user.is_staff is True:
            loans = myfilter.filter(
                Q(day=day_today)
                & Q(payment_plan="weekly")
                & Q(staff=self.request.user)
            ).select_related("staff", "client")
        context = {"loans": loans}
        return render(request, template_name, context)


class Clientportal(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transactions/listviews/clients-portal.html"


class Clearedloans(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/listviews/clearedloans.html"
        if self.request.user.is_admin is True:
            loans = Transaction.objects.filter(loan_amount__isnull=False)
            loans = loans.filter(
                Q(status="cleared") | Q(
                    status="not approved")
            ).select_related("staff", "client")
        if self.request.user.is_admin is False and self.request.user.is_staff is True:
            loans = Transaction.objects.filter(
                Q(loan_amount__isnull=False) & Q(staff=self.request.user)
            )
            loans = loans.filter(
                Q(status="cleared") |  Q(
                    status="not approved")
            ).select_related("staff", "client")
        paginated_loans = Paginator(loans, 10)
        page_number = request.GET.get("page")
        loans = paginated_loans.get_page(page_number)
        context = {
            "loans": loans,
        }
        return render(request, template_name, context)


class Clienthome(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/listviews/clients.html"
        clients = cache.get("clients")
        if clients is None:
            clients = Client.objects.select_related("staff")
            cache.set("clients", clients)
        paginated_clients = Paginator(clients, 10)
        page_number = request.GET.get("page")
        clients = paginated_clients.get_page(page_number)
        context = {"clients": clients, "form": Clientcreationform()}
        return render(request, template_name, context)


class Annualloanreport(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/business-reports/annual-loan-reports.html"

        loans = Transaction.objects.only(
            'loan_amount').filter(loan_amount__isnull=False)

        report_filter = Annualfilter(request.GET, queryset=loans)
        loans = report_filter.qs[:1]
        context = {"loans": loans, "report_filter": report_filter}
        return render(request, template_name, context)


class Monthlyloanreport(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/business-reports/monthly-loan-reports.html"
        loans = Transaction.objects.only(
            'loan_amount').filter(loan_amount__isnull=False)
        report_filter = Monthlyfilter(request.GET, queryset=loans)
        loans = report_filter.qs[:1]
        context = {"loans": loans, "report_filter": report_filter}
        return render(request, template_name, context)


class Generalloanreport(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/business-reports/general-loan-reports.html"

        loans = Transaction.objects.only('loan_amount','staff_id').filter(
            loan_amount__isnull=False)[:1]

        context = {"loans": loans}
        return render(request, template_name, context)


class Annualincomestatment(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/business-reports/annual-income-statement.html"
        reports = Transaction.objects.filter(loan_amount__isnull=False).select_related(
            "staff", "client"
        )
        report_filter = Annualfilter(request.GET, queryset=reports)
        reports = report_filter.qs[:1]
        context = {"reports": reports, "report_filter": report_filter}
        return render(request, template_name, context)


class Monthlyincomestatment(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/business-reports/monthly-income-statement.html"
        reports = Transaction.objects.filter(loan_amount__isnull=False).select_related(
            "staff", "client"
        )
        report_filter = Monthlyfilter(request.GET, queryset=reports)
        reports = report_filter.qs[:1]
        context = {"reports": reports, "report_filter": report_filter}
        return render(request, template_name, context)


class Cashflows(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/business-reports/cashflow.html"
        reports = Transaction.objects.filter(loan_amount__isnull=False).select_related(
            "staff", "client"
        )
        report_filter = Annualfilter(request.GET, queryset=reports)
        reports = report_filter.qs[:1]
        context = {"reports": reports, "report_filter": report_filter}
        return render(request, template_name, context)


class Balancesheet(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/business-reports/balance-sheet.html"
        loans = Transaction.objects.filter(loan_amount__isnull=False).select_related(
            "staff", "client"
        )[:1]

        context = {"loans": loans}
        return render(request, template_name, context)


class Annualsavingreport(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/business-reports/annual-savings-report.html"
        savings = Transaction.objects.filter(
            Q(initial_saving__isnull=False)
        ).select_related("staff", "client")
        report_filter = Annualfilter(request.GET, queryset=savings)
        savings = report_filter.qs[:1]
        context = {"savings": savings, "report_filter": report_filter}
        return render(request, template_name, context)


class Generalsavingreport(LoginRequiredMixin, View):
    def get(self, request):
        template_name = "transactions/business-reports/general-savings-reports.html"
        savings = Transaction.objects.filter(
            Q(initial_saving__isnull=False)
        ).select_related("staff", "client")[:1]

        context = {"savings": savings}
        return render(request, template_name, context)


class Help(ListView):
    model = Transaction
    template_name = "transactions/help.html"


def assetlinks(request):
    return render(request, ".well-known/assetlinks.json")


# ======================CREATE VIEWS=======================================


class C2BValidationAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = Paymentserializer
    permission_classes = [AllowAny]


class C2BConfirmationAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = Paymentserializer
    permission_classes = [AllowAny]


class Createpayment(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Payment
    template_name = "transactions/forms/create-payment.html"
    form_class = Addpaymentform
    success_message = "Payment added successfully"

    def form_valid(self, form):
        form.instance.staff = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        cache.delete_many(["payments", "loans"])
        return reverse("loans")


class Addexpense(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transaction
    template_name = "transactions/forms/add-expense.html"
    form_class = Addexpenseform
    success_message = "Payment added successfully"

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("expenses")


class Cashflowtransaction(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transaction
    template_name = "transactions/forms/cashflow-form.html"
    form_class = Cashflowform
    success_message = "Added successfully"

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("annual-cashflow-statement")


class Createloan(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transaction
    template_name = "transactions/forms/add-loan.html"
    form_class = Loancreationform
    success_message = "Loan added successfully"

    def form_valid(self, form):
        # form.instance.staff = self.request.user
        form.instance.staff = form.instance.staff
        return super().form_valid(form)

    def get_success_url(self):
        cache.delete("loans")
        return reverse("loans")


class Bulkcreateloans(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transaction
    template_name = "transactions/forms/bulk-add-loans.html"
    form_class = Loancreationform
    success_message = "Loans added successfully"

    def form_valid(self, form):
        form.instance.staff = form.instance.staff
        # form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        cache.delete("f-loans")
        return reverse("loans")


def add_loan_bulk_forms(request):
    template_name = "transactions/partials/bulk-loancreation-form-partial.html"
    return render(request, template_name, context={'form': Loancreationform()})


class Createclient(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Client

    template_name = "transactions/forms/add-client.html"
    form_class = Clientcreationform
    success_message = "Client added successfully"

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        cache.delete("clients")
        return reverse("clients")


class Bulkcreateloans(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transaction
    template_name = "transactions/forms/bulk-add-loans.html"
    form_class = Loancreationform
    success_message = "Loans added successfully"

    def form_valid(self, form):
        form.instance.staff = form.instance.staff
        # form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        cache.delete("loans")
        return reverse("loans")


class Bulkcreateclients(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Client
    template_name = "transactions/forms/bulk-add-clients.html"
    form_class = Clientcreationform
    success_message = "Clients added successfully"

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        cache.delete("clients")
        return reverse("clients")


class Bulkcreatepayment(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Payment
    template_name = "transactions/forms/bulk-add-payments.html"
    form_class = Addpaymentform
    success_message = "Payments added successfully"

    def form_valid(self, form):
        form.instance.staff = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        cache.delete_many(["payments", "loans"])
        return reverse("loans")


class Bulkaddexpense(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transaction
    template_name = "transactions/forms/bulk-add-expenses.html"
    form_class = Addexpenseform
    success_message = "Expenses added successfully"

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("expenses")


def add_loan_bulk_forms(request):
    template_name = "transactions/partials/bulkadd-loans-partial.html"
    return render(request, template_name, context={"form": Loancreationform()})


def add_client_bulk_forms(request):
    template_name = "transactions/partials/bulkadd-clients-partial.html"
    return render(request, template_name, context={"form": Clientcreationform()})


def add_payment_bulk_forms(request):
    template_name = "transactions/partials/bulkadd-payments-partial.html"
    return render(request, template_name, context={"form": Addpaymentform()})


def add_expense_bulk_forms(request):
    template_name = "transactions/partials/bulkadd-expenses-partial.html"
    return render(request, template_name, context={"form": Addexpenseform()})


# ==============================UPDATE VIEWS==============================================


class Editloanstatement(LoginRequiredMixin, UpdateView):
    model = Payment
    template_name = "transactions/forms/edit-payments.html"
    form_class = Paymenteditform
    context_object_name = "payment"

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        cache.delete_many(["payments", "loans"])
        return reverse("loans")


class Editcashflowtransaction(LoginRequiredMixin, UpdateView):
    model = Transaction
    template_name = "transactions/forms/edit-cashflow-form.html"
    form_class = Cashflowform
    context_object_name = "transaction"

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("annual-cashflow-statement")


class Editclient(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Client

    template_name = "transactions/forms/edit-client.html"
    form_class = Clientupdateform
    success_message = "Client updated successfully"
    context_object_name = "client"

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        cache.delete("clients")
        return reverse("clients")


class Editexpense(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Transaction
    template_name = "transactions/forms/edit-expense.html"
    form_class = Addexpenseform
    success_message = "Expense updated successfully"
    context_object_name = "expense"

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        cache.delete("expenses")
        return reverse("expenses")


class Editloan(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Transaction
    template_name = "transactions/forms/edit-loan.html"
    form_class = Loaneditform
    success_message = "Loan updated successfully"
    context_object_name = "loan"

    def form_valid(self, form):
        # form.instance.staff = self.request.user
        form.instance.staff = form.instance.staff
        return super().form_valid(form)

    def get_success_url(self):
        cache.delete("loans")
        return reverse("loans")


# ====================================BULK UPDATE VIEWS=======================================
@login_required
def update_payment_reason_to_penalties(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Payment.objects.filter(pk__in=checked_ids).update(
        payment_reason="penalties")
    payments = Payment.objects.filter(Q(amount__isnull=False)).select_related(
        "staff", "transaction__client", "transaction__staff"
    )
    loans = Transaction.objects.filter(
                    ~Q(status="not approved")
                  & ~Q(status="cleared")
                    & Q(loan_amount__isnull=False)
                ).select_related("staff","client")
    for loan in loans:
        loan.save()
    paginated_payments = Paginator(payments, 10)
    page_number = request.GET.get("page")
    payments = paginated_payments.get_page(page_number)
    context = {"payments": payments}
    cache.delete_many(["payments", "loans"])
    return render(request, "transactions/partials/payments-partial.html", context)


@login_required
def update_payment_reason_to_charges(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Payment.objects.filter(pk__in=checked_ids).update(payment_reason="charges")

    payments = Payment.objects.filter(Q(amount__isnull=False)).select_related(
        "staff", "transaction__client", "transaction__staff"
    )
    loans = Transaction.objects.filter(
                    ~Q(status="not approved")
                  & ~Q(status="cleared")
                    & Q(loan_amount__isnull=False)
                ).select_related("staff","client")
    for loan in loans:
        loan.save()
    paginated_payments = Paginator(payments, 10)
    page_number = request.GET.get("page")
    payments = paginated_payments.get_page(page_number)
    context = {"payments": payments}
    cache.delete_many(["payments", "loans"])

    return render(request, "transactions/partials/payments-partial.html", context)


@login_required
def update_payment_reason_to_loan_repayment(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Payment.objects.filter(pk__in=checked_ids).update(
        payment_reason="loan repayment")

    payments = Payment.objects.filter(Q(amount__isnull=False)).select_related(
        "staff", "transaction__client", "transaction__staff"
    )
    loans = Transaction.objects.filter(
                    ~Q(status="not approved")
                  & ~Q(status="cleared")
                    & Q(loan_amount__isnull=False)
                ).select_related("staff","client")
    for loan in loans:
        loan.save()
    paginated_payments = Paginator(payments, 10)
    page_number = request.GET.get("page")
    payments = paginated_payments.get_page(page_number)
    context = {"payments": payments}
    cache.delete_many(["payments", "loans"])
    return render(request, "transactions/partials/payments-partial.html", context)


# ====================BULK DELETE VIEWS========================================================
@login_required
def delete_loans(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Transaction.objects.filter(pk__in=checked_ids).delete()
    loans = Transaction.objects.filter(
                    ~Q(status="not approved")
                  & ~Q(status="cleared")
                    & Q(loan_amount__isnull=False)
                ).select_related("staff","client")
    paginated_loans = Paginator(loans, 10)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {
        "loans": loans,
    }
    cache.delete_many(["payments", "loans"])
    return render(request, "transactions/partials/loans-partial.html", context)


@login_required
def delete_payments(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Payment.objects.filter(pk__in=checked_ids).delete()
    payments = Payment.objects.filter(
        Q(TransAmount__isnull=False)
    ).select_related("staff", "transaction__client", "transaction__staff")
    paginated_payments = Paginator(payments, 10)
    page_number = request.GET.get("page")
    payments = paginated_payments.get_page(page_number)
    context = {"payments": payments}
    cache.delete_many(["payments", "loans"])
    return render(request, "transactions/partials/payments-partial.html", context)


@login_required
def delete_client(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Client.objects.filter(pk__in=checked_ids).delete()
    cache.delete("clients")
    clients = Client.objects.select_related("staff")
    paginated_clients = Paginator(clients, 12)
    page_number = request.GET.get("page")
    clients = paginated_clients.get_page(page_number)
    context = {"clients": clients}
    return render(request, "transactions/partials/clients-partial.html", context)


@login_required
def delete_expenses(request):
    context = {}
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    checked_ids = q.getlist("ids")
    Transaction.objects.filter(pk__in=checked_ids).delete()
    expenses = Transaction.objects.filter(expense_amount__isnull=False).select_related(
        "staff", "client"
    )

    paginated_clients = Paginator(expenses, 10)
    page_number = request.GET.get("page")
    expenses = paginated_clients.get_page(page_number)
    context = {"expenses": expenses, "form": Addexpenseform()}
    return render(request, "transactions/partials/expenses-partial.html", context)


@login_required
def delete_unapproved_loans(request):
    context = {}
    Transaction.objects.filter(status="not approved").delete()
    cache.clear()
    cleared_loans = Transaction.objects.filter(loan_amount__isnull=False)
    loans = cleared_loans.filter(
        Q(status="cleared")| Q(status="not approved")
    ).select_related("staff", "client")
    paginated_loans = Paginator(loans, 10)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {"loans": loans}
    return render(request, "transactions/partials/clearedloans-partial.html", context)


# ==================================SEARCH VIEWS========================================================


class Loansearch(LoginRequiredMixin, View):
    def get(self, request):

        loans = cache.get("loans")
        template = "transactions/partials/loans-partial.html"

        search = request.GET.get("search")
        if search:
            loans = loans.filter(
                Q(client__full_name__icontains=search)
                | Q(client__phone1__icontains=search)
                | Q(client__phone2__icontains=search)
                | Q(client__id_number__icontains=search)
                | Q(staff__first_name__icontains=search)

            )
        context = {
            "loans": loans,
        }

        return render(request, template, context)


class Paymentsearch(LoginRequiredMixin, View):
    def get(self, request):
        payments = cache.get("payments")
        search = request.GET.get("search")
        if search:
            payments = payments.filter(
                Q(transaction__client__full_name__icontains=search)
                | Q(transaction__client__phone1__icontains=search)
                | Q(transaction__client__id_number__icontains=search)
                | Q(payment_day__icontains=search)
            )
        context = {
            "payments": payments,
        }

        return render(request, "transactions/partials/payments-partial.html", context)


class Expensesearch(LoginRequiredMixin, View):
    def get(self, request):
        expenses = Transaction.objects.filter(
            expense_amount__isnull=False
        ).select_related("staff", "client")
        search = request.GET.get("search")
        if search:
            expenses = expenses.filter(
                Q(lending_date__icontains=search) | Q(
                    category__icontains=search)
            )
        context = {
            "expenses": expenses,
        }

        return render(request, "transactions/partials/expenses-partial.html", context)


class Clearedloansearch(LoginRequiredMixin, View):
    def get(self, request):
        myfilter = Transaction.objects.filter(loan_amount__isnull=False)
        loans = myfilter.filter(
            Q(status="cleared") |  Q(status="not approved")
        ).select_related("staff", "client")

        search = request.GET.get("search")
        if search:
            loans = loans.filter(
                Q(client__full_name__icontains=search)
                | Q(client__phone1__icontains=search)
                | Q(day__icontains=search)
                | Q(month_year__icontains=search)
            )
        context = {
            "loans": loans,
        }

        return render(
            request, "transactions/partials/clearedloans-partial.html", context
        )


class Clientsearch(LoginRequiredMixin, View):
    def get(self, request):
        clients = Client.objects.select_related("staff")
        search = request.GET.get("search")
        if search:
            clients = clients.filter(
                Q(full_name__icontains=search)
                | Q(phone1__icontains=search)
                | Q(id_number__icontains=search)
                | Q(phone2__icontains=search)
            )
        context = {
            "clients": clients,
        }
        return render(request, "transactions/partials/clients-partial.html", context)


@login_required
def expenses_audit(request):
    template_name = "transactions/business-reports/audit-trail/expenses-audit.html"

    expenses = Transaction.objects.filter(
        Q(expense_amount__isnull=False) | Q(loan_amount__isnull=False)
    ).select_related("staff", "client")
    paginated_expenses = Paginator(expenses, 20)
    page_number = request.GET.get("page")
    expenses = paginated_expenses.get_page(page_number)
    context = {"expenses": expenses}
    return render(request, template_name, context)


@login_required
def income_audit(request):
    template_name = "transactions/business-reports/audit-trail/income-audit.html"

    loans = Transaction.objects.filter(
        ~Q(status="not approved")
        & ~Q(status="waiting approval")
        & Q(loan_amount__isnull=False)
    ).select_related("staff", "client")
    paginated_loans = Paginator(loans, 20)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {"loans": loans}
    return render(request, template_name, context)


@login_required
def cash_in_audit(request):
    template_name = "transactions/business-reports/audit-trail/cashin-audit.html"
    myfilter = Transaction.objects.filter(
        ~Q(status="not approved") & ~Q(status="waiting approval")
    )
    loans = myfilter.filter(
        Q(loan_amount__isnull=False)
        | Q(expense_amount__isnull=False)
        | Q(transaction_amount__isnull=False)
    ).select_related("staff", "client")
    paginated_loans = Paginator(loans, 20)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {"loans": loans}
    return render(request, template_name, context)


@login_required
def cash_out_audit(request):
    template_name = "transactions/business-reports/audit-trail/cashout-audit.html"
    myfilter = Transaction.objects.filter(
        ~Q(status="not approved") & ~Q(status="waiting approval")
    )
    loans = myfilter.filter(
        Q(loan_amount__isnull=False)
        | Q(expense_amount__isnull=False)
        | Q(transaction_amount__isnull=False)
    ).select_related("staff", "client")

    paginated_loans = Paginator(loans, 20)
    page_number = request.GET.get("page")
    loans = paginated_loans.get_page(page_number)
    context = {"loans": loans}
    return render(request, template_name, context)


class income_audit_search(LoginRequiredMixin, View):
    def get(self, request):
        loans = Transaction.objects.filter(
            ~Q(status="not approved")
            & ~Q(status="waiting approval")
            & Q(loan_amount__isnull=False)
        ).select_related("staff", "client")
        search = request.GET.get("search")
        if search:
            loans = loans.filter(
                Q(year__icontains=search) | Q(month_year__icontains=search)
            )
        context = {
            "loans": loans,
        }
        return render(
            request, "transactions/partials/income-audit-partial.html", context
        )


class expense_audit_search(LoginRequiredMixin, View):
    def get(self, request):
        expenses = Transaction.objects.filter(
            expense_amount__isnull=False
        ).select_related("staff", "client")
        search = request.GET.get("search")
        if search:
            expenses = expenses.filter(
                Q(year__icontains=search) | Q(month_year__icontains=search)
            )
        context = {
            "expenses": expenses,
        }
        return render(
            request, "transactions/partials/expenses-audit-partial.html", context
        )


class cashin_audit_search(LoginRequiredMixin, View):
    def get(self, request):
        myfilter = Transaction.objects.filter(
            ~Q(status="not approved") & ~Q(status="waiting approval")
        )
        loans = myfilter.filter(
            Q(loan_amount__isnull=False)
            | Q(expense_amount__isnull=False)
            | Q(transaction_amount__isnull=False)
        ).select_related("staff", "client")
        search = request.GET.get("search")

        if search:
            loans = loans.filter(Q(year__icontains=search))
        context = {
            "loans": loans,
        }
        return render(
            request, "transactions/partials/cashin-audit-partial.html", context
        )


class cashout_audit_search(LoginRequiredMixin, View):
    def get(self, request):
        myfilter = Transaction.objects.filter(
            ~Q(status="not approved") & ~Q(status="waiting approval")
        )
        loans = myfilter.filter(
            Q(loan_amount__isnull=False)
            | Q(expense_amount__isnull=False)
            | Q(transaction_amount__isnull=False)
        ).select_related("staff", "client")

        search = request.GET.get("search")

        if search:
            loans = loans.filter(Q(year__icontains=search))
        context = {
            "loans": loans,
        }
        return render(
            request, "transactions/partials/cashout-audit-partial.html", context
        )
