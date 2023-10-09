
from django.contrib import admin
from .models import Transaction,Client,Payment
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class Transactionadmin(admin.ModelAdmin):
   
    list_display = ('client','loan_amount','status')
    search_fields = ('client','loan_amount','status')
    list_per_page = 80
    filter_horizontal = ()
    list_filter =()
    fieldsets = ()

class Clientadmin(ImportExportModelAdmin):
   
    list_display = ('full_name','phone1')
    search_fields = ('full_name','phone1')
    list_per_page = 80
    filter_horizontal = ()
    list_filter =()
    fieldsets = ()


class Paymentadmin(admin.ModelAdmin):
   
    list_display = ('BillRefNumber','TransID','amount')
    search_fields = ('BillRefNumber','TransID','amount')
    list_per_page = 80
    filter_horizontal = ()
    list_filter =()
    fieldsets = ()

admin.site.register(Transaction,Transactionadmin)

admin.site.register(Payment,Paymentadmin)
admin.site.register(Client,Clientadmin)





