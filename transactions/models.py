import sys
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property
from django.db.models import Sum, Q, F
from dateutil.relativedelta import relativedelta
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from django.db import transaction
from datetime import datetime
import calendar
from decimal import Decimal


def compress(image):
    if image.name != "default-id.jpg":
        imageTemp = Image.open(image)
        outputIoStream = BytesIO()
        myimage = imageTemp.resize((1020, 573))
        myimage.save(outputIoStream, format="JPEG", quality=60)
        outputIoStream.seek(0)
        new_image = InMemoryUploadedFile(
            outputIoStream,
            "ImageField",
            "%s.jpg" % image.name.split(".")[0],
            "image/jpeg",
            sys.getsizeof(outputIoStream),
            None,
        )
        return new_image
    return "default-id.jpg"


class Client(models.Model):
    full_name = models.CharField(max_length=200, blank=True, null=True)
    phone1 = models.CharField(max_length=200, blank=True, null=True)
    employer_or_business_type = models.CharField(
        max_length=200, blank=True, null=True)
    id_number = models.CharField(max_length=200, blank=True, null=True)

    phone2 = models.CharField(max_length=200, blank=True, null=True)

    location = models.CharField(max_length=200, blank=True, null=True)
    
    employers_phone = models.CharField(max_length=200, blank=True, null=True)

    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    registration_date = models.DateTimeField(default=timezone.now)
    id_front = models.ImageField(
        null=True, blank=True, default="default-id.jpg")
    id_back = models.ImageField(
        null=True, blank=True, default="default-id.jpg")

    class Meta:
        ordering = ["-registration_date"]

    def get_absolute_url(self):
        return reverse("clients")

    def __str__(self):
        return f"({self.full_name})(Id,{self.id_number})(phone,{self.phone1})"

    def save(self, *args, **kwargs):
        new_image = compress(self.id_front)
        self.id_front = new_image
        new_image = compress(self.id_back)
        self.id_back = new_image
        super().save(*args, **kwargs)


class Transaction(models.Model):
    STATUS = (
        ("cleared", "cleared"),
        ("approved", "approved"),
        ("not approved", "not approved"),
        ("overdue", "overdue"),
        ("rolled over", "rolled over"),
    )
  

    EXPENSES = (
        ("salaries", "salaries"),
        ("legal", "legal"),
        ("auctioneer fee", "auctioneer fee"),
        ("imprest", "imprest"),
        ("marketing", "marketing"),
        ("airtime", "airtime"),
        ("miscellaneous", "miscellaneous"),
        ("assets depreciation", "assets depreciation"),
        ("loan interest", "loan interest"),
        ("dividends", "dividends"),
        ("loan payment", "loan payment"),
        ("administration", "administration"),
        ("audit", "audit"),
        ("transport", "transport"),
        ("system", "system"),


    )
    TRANSACTION_ITEMS = (
        ("ob", "opening balance"),
        ("cfs", "capital from shareholders"),
        ("lf", "long term loans"),
        ("ow", "owner withdrawals"),
        ("ppe", "plant property equipment"),
        ("ae", "accrued expenses"),
        ("ap", "accounts payable"),
        ("re", "retained earnings"),
        ("di", "dividends payable"),
       
    )

    PAYMENT_PLAN = (
        ("weekly", "weekly"),
        ("monthly", "monthly"),

    )
    MODE_OF_PAYMENT = (
        ("mpesa", "mpesa"),
        ("bank", "bank"),
        ("cash", "cash"),
    )

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(
        max_length=100, blank=True, choices=STATUS, default="approved"
    )
    payment_plan = models.CharField(
        max_length=100, blank=True, null=True, choices=PAYMENT_PLAN, default="weekly",verbose_name="Repayment shedule"
    )
   
    loan_amount = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )
    interest_rate = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10,default=20.00
    )
    payable_amount = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )
    installment = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )
    outstanding_loan = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )
    interest_charged = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )
    processing_fee = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )
    penalties_payment = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )

    registration = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )

   
    period_in_months = models.IntegerField(default=1, null=True, blank=True)

    arrears = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10,default=0.00
    )
    transaction_description = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=TRANSACTION_ITEMS,
        verbose_name="description",
    )
    repayments = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )
    rollovers= models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10)
    lending_date = models.DateTimeField(default=timezone.now)
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    year = models.CharField(max_length=50, null=True, blank=True)
    month_year = models.CharField(max_length=50, null=True, blank=True)
    day_month_year = models.CharField(max_length=50, null=True, blank=True)
    day = models.CharField(max_length=50, null=True, blank=True)
    expense_amount = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )
    transaction_amount = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )
    transaction_description = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=TRANSACTION_ITEMS,
        verbose_name="description",
    )
    category = models.CharField(
        max_length=50, null=True, blank=True, choices=EXPENSES)
    notes = models.CharField(max_length=500, null=True, blank=True)
    mode_of_payment = models.CharField(
        max_length=200, null=True, blank=True, choices=MODE_OF_PAYMENT, default="mpesa"
    )

    class Meta:
        ordering = ["-lending_date"]
        indexes = [
            models.Index(
                fields=[
                    "status",
                    "loan_amount",
                    "transaction_description",
                    "year",
                    "month_year",
                    "day_month_year",
                    "-lending_date",
                ]
            ),
        ]

    def __str__(self):
        return f"{self.client},(outstanding {self.outstanding_loan})(installment {self.installment})"

    # ================================loans duration calculation=================================
    @cached_property
    def year_calculation(self):
        lending_year = self.lending_date.year
        return str(lending_year)
    @cached_property
    def day_to_display(self):
        return self.day_calculation[:3]
   
    @cached_property
    def month_calculation(self):
        lending_month = self.lending_date.month
        return str(lending_month)

    @cached_property
    def month_year_calculation(self):
        return f"{self.month_calculation}/{self.year_calculation}"

    @cached_property
    def day_calculation(self):
        loan_day = calendar.day_name[self.lending_date.weekday()]
        return str(loan_day)

    @cached_property
    def due_date(self):
        if self.loan_amount is not None:
            date = self.lending_date
            due_date = date + relativedelta(months=+self.period_in_months)
            return due_date

    @cached_property
    def interest_calculation(self):
        if self.loan_amount:
            interest = self.loan_amount * (self.interest_rate / 100)
            interest = Decimal(interest * self.period_in_months) 
            return interest * self.period_in_months

    
    @cached_property
    def processing_fee_calculation(self):
        if self.loan_amount:
           return self.loan_amount * Decimal(0.05)

    

    @cached_property
    def disbursed_amount(self):
        if self.loan_amount:
            return round(self.loan_amount - self.processing_fee_calculation - self.registration, 2)

       
    @cached_property
    def payable_amount_calculation(self):
        if self.loan_amount:
            return round(self.loan_amount + self.interest_calculation, 2)

    @cached_property
    def loan_repayments_calculation(self):
        result = Transaction.objects.filter(
            id=self.id, payment__payment_reason="loan repayment"
        ).aggregate(total=Sum("payment__amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def rollover_charges_calculation(self):
        result = Transaction.objects.filter(
            id=self.id, payment__payment_reason="rollover charges"
        ).aggregate(total=Sum("payment__amount", default=0))
        return result["total"]

   

    @cached_property
    def penalties_paid_calculation(self):
        result = Transaction.objects.filter(
            id=self.id, payment__payment_reason="penalties"
        ).aggregate(total=Sum("payment__amount", default=0))
        return result["total"]

    @cached_property
    def loan_aging_calculation(self):
        today = datetime.today().date()
        due = self.due_date.date()
        days_to_due = due - today
        days = days_to_due.days
        if days == 0:
            return "due today"
        if days > 0:
            return f"Due in {days} days"

        if days < 0:
            return f"Ovedue by {abs(days)} days"

    # ===========INSTALLMENTS CALCULATION====================================

    @cached_property
    def penalties_balance(self):
        if self.loan_amount:
            today = datetime.today().date()
            due = self.due_date.date()
            days_to_due = due - today
            days = days_to_due.days
            if days == 0:
                return 0
            if days < 0:
                return abs(days * 500)
            if days > 0:
                return 0

    @cached_property
    def installment_calculation(self):
        if self.loan_amount:
            period = self.period_in_months
            period_in_weeks = round(self.period_in_months * Decimal(4.345))
            payable_amount = self.payable_amount_calculation
            if self.payment_plan == "monthly":
                return round(payable_amount/period, 2)
            
            if self.payment_plan == "weekly":
                
                return round(payable_amount / period_in_weeks, 2)

    
    @cached_property
    def outstanding_loan_calculation(self):
        payable_loan = self.payable_amount_calculation
        repayments = self.loan_repayments_calculation
        if payable_loan is None:
            payable_loan = 0
        if repayments is None:
            repayments = 0
        balance = payable_loan - repayments
        return round(balance, 2)

    @cached_property
    def arrears_calculations(self):
        if self.status == 'overdue' or self.status == 'bad debt':
            arrears = self.outstanding_loan_calculation
            return arrears
        else:
            return self.arrears

    @cached_property
    def day_month_year_calculation(self):
        if self.loan_amount:
            return f"{self.due_date.day}/{self.due_date.month}/{self.due_date.year}"

    def save(self, *args, **kwargs):
        self.repayments = self.loan_repayments_calculation
        self.arrears = self.arrears_calculations
     
        self.installment = self.installment_calculation
        self.outstanding_loan = self.outstanding_loan_calculation
        self.penalties_payment = self.penalties_paid_calculation
        self.processing_fee = self.processing_fee_calculation
        self.payable_amount = self.payable_amount_calculation
        self.year = self.year_calculation
        self.month_year = self.month_year_calculation
        self.day_month_year = self.day_month_year_calculation
        self.interest_charged = self.interest_calculation
        self.day = self.day_calculation
        self.rollovers = self.rollover_charges_calculation
        super(Transaction, self).save(*args, **kwargs)

    # =============================staff reports============================================     #

    @cached_property
    def total_staff_outstandings(self):
        result = Transaction.objects.filter(staff=self.staff).aggregate(
            total=Sum("outstanding_loan", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_staff_arrears(self):
        result = Transaction.objects.filter(
            staff=self.staff).aggregate(total=Sum("arrears", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_staff_repayments(self):
        result = Transaction.objects.filter(staff=self.staff).aggregate(
            total=Sum("repayments", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_staff_payables(self):
        result = Transaction.objects.filter(staff=self.staff).aggregate(
            total=Sum("payable_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_staff_payments_collectable(self):
        myfilter = Transaction.objects.filter(Q(staff=self.staff))
        result = myfilter.filter(
            Q(status="approved") | Q(status="rolled over")
        ).aggregate(total=Sum("installment", default=0))
        return round(result["total"], 2)

    @cached_property
    def staff_portfolio_at_risk(self):
        arrears = self.total_arrears
        outstandings = self.total_outstandings
        if arrears != 0.00 and outstandings > 0.00:
            total = arrears / outstandings

            percentage = "{:.2%}".format(total)
            return percentage
        else:
            return 0.00

    # ==================================== GENERAL LOAN REPORTS===========================
    @cached_property
    def total_loans(self):
        result = Transaction.objects.aggregate(
            total=Sum("loan_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_interest_charged(self):
        result = Transaction.objects.aggregate(
            total=Sum("interest_charged", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_payable_loans(self):
        result = Transaction.objects.aggregate(
            total=Sum("payable_amount", default=0))

        return round(result["total"], 2)

    @cached_property
    def total_repayments(self):
        result = Transaction.objects.aggregate(
            total=Sum("repayments", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_outstandings(self):
        result = Transaction.objects.aggregate(
            total=Sum("outstanding_loan", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_arrears(self):
        result = Transaction.objects.aggregate(total=Sum("arrears", default=0))

        return round(result["total"], 2)

    @cached_property
    def portfolio_at_risk(self):
        arrears = self.total_arrears
        outstandings = self.total_outstandings
        if arrears != 0.00 and outstandings > 0.00:
            total = arrears / outstandings

            percentage = "{:.2%}".format(total)
            return percentage
        return 0

    # ========== =================================== ANNUAL LOAN REPORTS===========================

    @cached_property
    def total_annual_loans(self):
        result = Transaction.objects.filter(year=self.year).aggregate(
            total=Sum("loan_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_annual_interest_charged(self):
        result = Transaction.objects.filter(year=self.year).aggregate(
            total=Sum("interest_charged", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_annual_payable_loans(self):
        result = Transaction.objects.filter(year=self.year).aggregate(
            total=Sum("payable_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_annual_repayments(self):
        result = Transaction.objects.filter(year=self.year).aggregate(
            total=Sum("repayments", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_annual_outstandings(self):
        result = Transaction.objects.filter(year=self.year).aggregate(
            total=Sum("outstanding_loan", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_annual_arrears(self):
        result = Transaction.objects.filter(
            year=self.year).aggregate(total=Sum("arrears", default=0))
        return round(result["total"], 2)

    @cached_property
    def annual_portfolio_at_risk(self):
        arrears = self.total_annual_arrears
        outstandings = self.total_annual_outstandings
        if arrears != 0.00 and outstandings > 0.00:
            total = arrears / outstandings

            percentage = "{:.2%}".format(total)
            return percentage
        return 0

    # ======== =================================== MONTHLY LOAN REPORTS===========================

    @cached_property
    def total_monthly_loans(self):
        result = Transaction.objects.filter(month_year=self.month_year).aggregate(
            total=Sum("loan_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_monthly_interest_charged(self):
        result = Transaction.objects.filter(month_year=self.month_year).aggregate(
            total=Sum("interest_charged", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_monthly_payable_loans(self):
        result = Transaction.objects.filter(month_year=self.month_year).aggregate(
            total=Sum("payable_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_monthly_repayments(self):
        result = Transaction.objects.filter(month_year=self.month_year).aggregate(
            total=Sum("repayments", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_monthly_outstandings(self):
        result = Transaction.objects.filter(month_year=self.month_year).aggregate(
            total=Sum("outstanding_loan", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_monthly_arrears(self):
        result = Transaction.objects.filter(
            month_year=self.month_year).aggregate(total=Sum("arrears", default=0))
        return round(result["total"], 2)

    @cached_property
    def monthly_portfolio_at_risk(self):
        arrears = self.total_arrears
        outstandings = self.total_outstandings
        if arrears != 0.00 and outstandings > 0.00:
            total = arrears / outstandings

            percentage = "{:.2%}".format(total)
            return percentage
        return 0

    # ====== ===================================ANNUAL INCOME STATEMENT==========================

    @cached_property
    def interest_income(self):
        result = Transaction.objects.filter(
            Q(year=self.year)
            & ~Q(status="not approved")

        ).aggregate(total=Sum("interest_charged", default=0))
        return round(result["total"], 2)

    @cached_property
    def processing_fee_income(self):
        result = Transaction.objects.filter(
            Q(year=self.year)
            & ~Q(status="not approved")

        ).aggregate(total=Sum("processing_fee", default=0))
        return round(result["total"], 2)

    @cached_property
    def loan_registration(self):
        result = Transaction.objects.filter(
            Q(year=self.year)
            & ~Q(status="not approved")

        ).aggregate(total=Sum("registration", default=0))
        return round(result["total"], 2)

    @cached_property
    def total_rollover_charges(self):
        result = Transaction.objects.filter(Q(year=self.year)).aggregate(
            total=Sum("rollovers", default=0)
        )
        return round(result["total"], 2)

   


    @cached_property
    def penalties_income(self):
        result = Transaction.objects.filter(Q(year=self.year)).aggregate(
            total=Sum("penalties_payment", default=0)
        )
        return round(result["total"], 2)

    @cached_property
    def income_before_all_expenses(self):
        return (
            self.interest_income
            + self.processing_fee_income
            + self.loan_registration
            + self.penalties_income
            + self.total_rollover_charges
            
        )

    # ================================expenses====================================================

    @cached_property
    def total_expenses(self):
        result = Transaction.objects.filter(year=self.year).aggregate(
            total=Sum("expense_amount", default=0)
        )
        return round(result["total"], 2)

    @cached_property
    def income_after_expenses(self):
        method1 = self.income_before_all_expenses
        method2 = self.total_expenses
        return method1 - method2

    # ====================MONTHLY INCOME STATEMENT===================================
    @cached_property
    def monthly_interest_income(self):
        result = Transaction.objects.filter(
            Q(month_year=self.month_year)
            & ~Q(status="not approved")

        ).aggregate(total=Sum("interest_charged", default=0))
        return round(result["total"], 2)

    @cached_property
    def monthly_processing_fee_income(self):
        result = Transaction.objects.filter(Q(month_year=self.month_year)).aggregate(
            total=Sum("processing_fee", default=0)
        )
        return round(result["total"], 2)

    @cached_property
    def monthly_registration(self):
        result = Transaction.objects.filter(
            Q(month_year=self.month_year)
            & ~Q(status="not approved")

        ).aggregate(total=Sum("registration", default=0))
        return round(result["total"], 2)

  


    @cached_property
    def monthly_rollover_charges(self):
        result = Transaction.objects.filter(Q(month_year=self.month_year)).aggregate(
            total=Sum("rollovers", default=0)
        )
        return round(result["total"], 2)

    @cached_property
    def monthly_penalties(self):
        result = Transaction.objects.filter(Q(month_year=self.month_year)).aggregate(
            total=Sum("penalties_payment", default=0)
        )
        return round(result["total"], 2)

    @cached_property
    def monthly_income_before_all_expenses(self):
        return (
            self.monthly_interest_income
            + self.monthly_registration
            + self.monthly_processing_fee_income
            + self.monthly_penalties
            + self.monthly_rollover_charges
           
        )

    # ================================expenses====================================================

    @cached_property
    def monthly_total_expenses(self):
        result = Transaction.objects.filter(month_year=self.month_year).aggregate(
            total=Sum("expense_amount", default=0)
        )
        return round(result["total"], 2)

    @cached_property
    def monthly_income_after_expenses(self):
        method1 = self.monthly_income_before_all_expenses
        method2 = self.monthly_total_expenses
        return method1 - method2


# ========================CASHFLOW FROM OPERATING ACTIVITIES===========================

    @cached_property
    def total_cashflow_payments(self):
        result = Transaction.objects.aggregate(
            total=Sum("repayments", default=0)
        )
        return round(result["total"], 2)

    @cached_property
    def total_cashflow_charges(self):
        result = Transaction.objects.aggregate(
            total=Sum("rollovers", default=0)
        )
        return round(result["total"], 2)

    @cached_property
    def cashflow_cash_at_beginning_of_the_period(self):
        result = Transaction.objects.filter(
            Q(transaction_description="ob")
        ).aggregate(total=Sum("transaction_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def cashflow_penalties(self):
        result = Transaction.objects.aggregate(
            total=Sum("penalties_payment", default=0)
        )
        return round(result["total"], 2)

    @cached_property
    def cashflow_expenses(self):
        result = Transaction.objects.aggregate(
            total=Sum("expense_amount", default=0)
        )
        return round(result["total"], 2)

    @cached_property
    def cashflow_disbursements(self):
        result = Transaction.objects.filter(
            ~Q(status="not approved")


        ).aggregate(
            total=Sum("loan_amount", default=0)
            - Sum("registration", default=0)
            - Sum("processing_fee", default=0)
          

        )
        return round(result["total"], 2)

    @cached_property
    def net_cashflow_from_operations(self):
        return (
            (
                self.cashflow_cash_at_beginning_of_the_period
                + self.total_cashflow_payments
                + self.cashflow_penalties
             + self.total_cashflow_charges
            )
            - self.cashflow_disbursements
            - self.cashflow_expenses
        )

 # =========================CASHFLOW FROM FINANCING ACTIVITIES===========================

    @cached_property
    def cashflow_owner_capital_injection(self):
        result = Transaction.objects.filter(
            Q(transaction_description="cfs")
        ).aggregate(total=Sum("transaction_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def cashflow_loan_injection(self):
        result = Transaction.objects.filter(
            Q(transaction_description="lf")
        ).aggregate(total=Sum("transaction_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def cashflow_drawings(self):
        result = Transaction.objects.filter(
            Q(transaction_description="ow")
        ).aggregate(total=Sum("transaction_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def net_cashflow_from_financing(self):
        return (
            self.cashflow_owner_capital_injection
            + self.cashflow_loan_injection
            - self.cashflow_drawings
        )

    @cached_property
    def cashflow_cash_balance(self):
        return self.net_cashflow_from_operations + self.net_cashflow_from_financing

    # ================================balance sheet============================================

    @cached_property
    def cash_and_cash_equivalents(self):
        return self.cashflow_cash_balance

    @cached_property
    def ppe(self):
        result = Transaction.objects.filter(
            Q(transaction_description="ppe")
        ).aggregate(total=Sum("transaction_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def loan_portfolio(self):
        return self.cashflow_disbursements

    @cached_property
    def total_assets(self):
        return self.cash_and_cash_equivalents + self.loan_portfolio + self.ppe

    # =====================liabilities===================
    @cached_property
    def accrued_expenses(self):
        result = Transaction.objects.filter(
            Q(transaction_description="ae")
        ).aggregate(total=Sum("transaction_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def accounts_payable(self):
        result = Transaction.objects.filter(
            Q(transaction_description="ap")
        ).aggregate(total=Sum("transaction_amount", default=0))
        return round(result["total"], 2)

    @cached_property
    def long_term_loans(self):
        return self.cashflow_loan_injection

    @cached_property
    def liabilities(self):
        return (
            self.long_term_loans

            + self.accounts_payable
            + self.accrued_expenses
        )

    @cached_property
    def equity(self):
        return self.total_assets - self.liabilities

    @cached_property
    def equity_liabilities(self):
        return self.equity + self.liabilities


class Payment(models.Model):
    PAYMENT_REASON = (
        ("loan repayment", "loan repayment"),
        ("penalties", "penalties"),
        ("charges", "charges"),
       
        
    )
    MODE_OF_PAYMENT = (
        ("mpesa", "mpesa"),
        ("bank", "bank"),
        ("cash", "cash"),
    )

    TransID = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Reference"
    )
    TransAmount = models.CharField(max_length=200, null=True, blank=True)
    withdraws = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2
    )
    MSISDN = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Phone"
    )
    payment_day= models.CharField(
        max_length=15, blank=True, null=True
    )
    BillRefNumber = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Id number", default="000000"
    )
    payment_reason = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        choices=PAYMENT_REASON,
        default="loan repayment",
    )
    mode_of_payment = models.CharField(
        max_length=200, null=True, blank=True, choices=MODE_OF_PAYMENT, default="mpesa"
    )
    amount = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2)
    send_sms = models.BooleanField(default=False)
    arrear_increment = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2
    )
    arrear_payment = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2
    )
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments",
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Search by name/id",
    )
    payment_date = models.DateTimeField(default=timezone.now)
    notes = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ["-payment_date"]
        indexes = [
            models.Index(
                fields=[
                    "payment_reason",
                    "-payment_date",
                ]
            ),
        ]

    def get_absolute_url(self):
        return reverse("payments")

    @cached_property
    def date_today(self):
        date = datetime.now()
        return date
    @cached_property
    def day_month_calculation(self):
        
        return f"{self.payment_date.day}/{self.payment_date.month}/{self.payment_date.year}"
    
    @cached_property
    def payment_amount(self):
        amount = round(self.TransAmount, 2)
        return amount

    @cached_property
    def arrear_payment_calculation(self):
        if self.transaction is not None and self.TransAmount is not None:
            with transaction.atomic():
                if self.transaction.arrears > 0.00:
                    amount = Decimal(self.TransAmount)
                    arrears = Transaction.objects.get(pk=self.transaction.id)
                    balance = amount - arrears.arrears
                    if amount >= arrears.arrears:
                        arrears.arrears = F('arrears') - arrears.arrears
                        arrears.save()

                        arrears.refresh_from_db()
                    if amount < arrears.arrears:
                        arrears.arrears = F('arrears') - amount
                        arrears.save()
                        arrears.refresh_from_db()
            with transaction.atomic():
                if self.transaction.arrears == 0.00:
                    amount = Decimal(self.TransAmount)
                    installment = Transaction.objects.get(
                        pk=self.transaction.id)
                    balance = installment.installment - amount

                    if amount < installment.installment:
                        installment.arrears = F('arrears') + balance
                        installment.save()
                        installment.refresh_from_db()

        if self.transaction is None:
            pass

    @cached_property
    def loan_payment_calculation(self):
        if self.transaction is not None and self.TransAmount is not None:
            amount = Decimal(self.TransAmount)
            return amount
        if self.transaction is None:
            pass

    def save(self, *args, **kwargs):
        self.amount = self.loan_payment_calculation
        self.payment_day = self.day_month_calculation
        self.arrear_payment = self.arrear_payment_calculation
        cache.delete_many(["payments", "loans"])

        super(Payment, self).save(*args, **kwargs)
