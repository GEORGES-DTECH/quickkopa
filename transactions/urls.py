from django.urls import path
from .views import (
    Createloan,
    Loandetail,
    Editloan,
    Editexpense,
    Addexpense,
    Annualloanreport,
    Loansearch,
    Annualincomestatment,
    Cashflows,
    Paymentsearch,
    Expensesearch,
    Clearedloansearch,
    Generalloanreport,
    Monthlyincomestatment,
    Loanview,
    Expenses,
    Clearedloans,
    Createclient,
    Cashflowtransaction,
    Editclient,
    Clienthome,
    Clientsearch,
    Clientdetail,
    Clientsdocuments,

    clear_loans,

    reverse_loans,
    delete_loans,
    delete_unapproved_loans,
    delete_client,
   
    loan_statement,
    Clientautocomplete,
    Staffautocomplete,
    Clientloanautocomplete,
    C2BConfirmationAPIView,
    C2BValidationAPIView,
    Cashflowtransactions,
    Paymentsview,
    delete_expenses,
    Editcashflowtransaction,
    Editloanstatement,
    Createpayment,
    Clientportal,
    update_payment_reason_to_loan_repayment,
    update_payment_reason_to_penalties,
    update_payment_reason_to_charges,
    Staffreport,
    approve_loans,
    disapprove_loans,
    rollover_loans,
    Monthlyloanreport,
    Overdueloansview,
    Monthlyloansduetoday,

    Weeklyloansduetoday,
    update_payments,
    update_loans,

    income_audit,
    income_audit_search,
    expenses_audit,
    expense_audit_search,
    cash_in_audit,
    cash_out_audit,
    cashin_audit_search,
    cashout_audit_search,
    Bulkcreateloans,
    add_loan_bulk_forms,
    Bulkcreateclients,
    add_client_bulk_forms,
    Bulkcreatepayment,
    add_payment_bulk_forms,
    Balancesheet,

    Bulkaddexpense,
    add_expense_bulk_forms,
    loan_history,
    delete_payments,

)

urlpatterns = [
    path(
        "client-autocomplete", Clientautocomplete.as_view(), name="client-autocomplete"
    ),
    path("staff-autocomplete", Staffautocomplete.as_view(),
         name="staff-autocomplete"),
    path(
        "client-loan-autocomplete",
        Clientloanautocomplete.as_view(),
        name="client-loan-autocomplete",
    ),

    #   =========================CREATE VIEWS=================================
    path("create-loan", Createloan.as_view(), name="create-loan"),
    path("bulk-create-loans", Bulkcreateloans.as_view(), name="bulk-create-loans"),
    path(
        "bulk-create-clients", Bulkcreateclients.as_view(), name="bulk-create-clients"
    ),
    path(
        "bulk-create-payments", Bulkcreatepayment.as_view(), name="bulk-create-payments"
    ),

    path("bulk-expenses", Bulkaddexpense.as_view(), name="bulk-create-expenses"),

    path("add-loan-forms", add_loan_bulk_forms, name="add-loan-forms"),
    path("add-expense-forms", add_expense_bulk_forms, name="add-expense-forms"),
    path("add-client-forms", add_client_bulk_forms, name="add-client-forms"),
    path("add-payment-forms", add_payment_bulk_forms, name="add-payment-forms"),


    path("transact", Cashflowtransaction.as_view(), name="transact"),
    path("add-expense", Addexpense.as_view(), name="add-expense"),

    path("create-client", Createclient.as_view(), name="create-client"),

    path("createpayment/", Createpayment.as_view(), name="create-payment"),
    path("validation/", C2BValidationAPIView.as_view(), name="validation"),
    path("confirmation/", C2BConfirmationAPIView.as_view(), name="confirmation"),
    #   =========================UPDATE VIEWS=================================
    path("edit-client/<int:pk>", Editclient.as_view(), name="edit-client"),
    path(
        "edit-cashflow-transaction/<int:pk>",
        Editcashflowtransaction.as_view(),
        name="edit-transaction",
    ),

    path("edit-loan/<int:pk>", Editloan.as_view(), name="edit-loan"),
    path("edit-expense/<int:pk>", Editexpense.as_view(), name="edit-expense"),
    path("edit/<int:pk>/", Editloanstatement.as_view(), name="edit-payment"),
    path("clear-loans", clear_loans, name="clear-loans"),
    path("approve-loans", approve_loans, name="approve-loans"),
    path("loan-history/<int:pk>/", loan_history, name="loan-history"),
    path("disapprove-loans", disapprove_loans, name="disapprove-loans"),
    path("rollover-loans", rollover_loans, name="rollover-loans"),
    path("reverse-loans", reverse_loans, name="reverse-loans"),
    path("update-payments", update_payments, name="update-payments"),
    path("update-loans", update_loans, name="update-loans"),
    path(
        "payment-is-penalties",
        update_payment_reason_to_penalties,
        name="payment-is-penalties",
    ),
    path(
        "payment-is-charges",
        update_payment_reason_to_charges,
        name="payment-is-charges",
    ),
    path(
        "payment-is-loan-repayment",
        update_payment_reason_to_loan_repayment,
        name="payment-is-loan-repayment",
    ),
    # =============================HOME VIEWS====================================
    path("", Loanview.as_view(), name="loans"),

    path("overdue-loans/", Overdueloansview.as_view(), name="overdue-loans"),
    path(
        "due-today-monthly-loans/", Monthlyloansduetoday.as_view(), name="todays-loans"
    ),
    path(
        "due-today-weekly-loans/",
        Weeklyloansduetoday.as_view(),
        name="weekly-todays-loans",
    ),
    path("portal/", Clientportal.as_view(), name="portal"),
    path(
        "annual-loan-reports/", Annualloanreport.as_view(), name="annual-loan-reports"
    ),
    path(
        "monthly-loan-reports/",
        Monthlyloanreport.as_view(),
        name="monthly-loan-reports",
    ),
    path(
        "annual-income-statement/",
        Annualincomestatment.as_view(),
        name="annual-income-statement",
    ),
    path(
        "monthly-income-statement/",
        Monthlyincomestatment.as_view(),
        name="monthly-income-statement",
    ),

    path(
        "balance-sheet/",
        Balancesheet.as_view(),
        name="balance-sheet",
    ),
    path(
        "cashflows/",
        Cashflows.as_view(),
        name="cashflows",
    ),
    path(
        "general-loan-reports/",
        Generalloanreport.as_view(),
        name="general-loan-reports",
    ),
    path("clients/", Clienthome.as_view(), name="clients"),
    path("expenses/", Expenses.as_view(), name="expenses"),
    path("cleared-loans/", Clearedloans.as_view(), name="cleared-loans"),
    path(
        "cashflow-transactions/",
        Cashflowtransactions.as_view(),
        name="cashflow-transactions",
    ),
    path("payments/", Paymentsview.as_view(), name="payments"),
    #    =======================DETAIL URLS===========================
    path("loan-statement/<int:pk>/", loan_statement, name="loan-statement"),
    path("loan-detail/<int:pk>/", Loandetail.as_view(), name="loan-detail"),
    path("client-detail/<int:pk>/", Clientdetail.as_view(), name="client-detail"),
    path("client-documents/<int:pk>/",
         Clientsdocuments.as_view(), name="client-docs"),
    path("staff-report/<int:pk>/", Staffreport.as_view(), name="staff-report"),

    #    =====================================SEARCH URLS==============================
    path("loan-search", Loansearch.as_view(), name="search-loans"),

    path(
        "cleared-loan-search", Clearedloansearch.as_view(), name="search-cleared-loans"
    ),
    path("search-payment", Paymentsearch.as_view(), name="search-payment"),
    path("search-expenses", Expensesearch.as_view(), name="search-expenses"),
    path("clientsearch", Clientsearch.as_view(), name="client-search"),
    #    ==============================DELETE================================
    path("delete-loans", delete_loans, name="delete-loans"),
    path("delete-payments", delete_payments, name="delete-payments"),
    path("delete-unapproved", delete_unapproved_loans,
         name="delete-unapproved-loans"),
    path("delete-clients", delete_client, name="delete-clients"),
    path("delete-expenses", delete_expenses, name="delete-expenses"),
    path("income-audit/", income_audit, name="income-audit"),
    path(
        "income-audit-search/",
        income_audit_search.as_view(),
        name="income-audit-search",
    ),
    path(
        "expense-audit-search/",
        expense_audit_search.as_view(),
        name="expense-audit-search",
    ),
    path("expenses-audit/", expenses_audit, name="expense-audit"),
    path("cashin-audit/", cash_in_audit, name="cashin-audit"),
    path("cashout-audit/", cash_out_audit, name="cashout-audit"),
    path(
        "cashin-audit-search/",
        cashin_audit_search.as_view(),
        name="cashin-audit-search",
    ),
    path(
        "cashout-audit-search/",
        cashout_audit_search.as_view(),
        name="cashout-audit-search",
    ),
]
