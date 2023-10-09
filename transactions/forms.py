from django import forms


from .models import Transaction, Client, Payment
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from django_select2.forms import ModelSelect2Widget


class ClientWidget(ModelSelect2Widget):
    search_fields = [
        "full_name__icontains",
        "phone1__icontains",
        "id_number__icontains",
        "phone1__icontains",
    ]

    def __init__(self, *args, **kwargs):
        kwargs["data_view"] = "client-autocomplete"
        super(ClientWidget, self).__init__(*args, **kwargs)


class ClientloanWidget(ModelSelect2Widget):
    search_fields = [
        "client__full_name__icontains",
        "client__phone1__icontains",
        "client__phone2__icontains",
        "client__id_number__icontains",
    ]

    def __init__(self, *args, **kwargs):
        kwargs["data_view"] = "client-loan-autocomplete"
        super(ClientloanWidget, self).__init__(*args, **kwargs)


class ClientsavingWidget(ModelSelect2Widget):
    search_fields = [
        "client__full_name__icontains",
        "client__phone1__icontains",
        "client__phone2__icontains",
        "client__id_number__icontains",
    ]

    def __init__(self, *args, **kwargs):
        kwargs["data_view"] = "client-saving-autocomplete"
        super(ClientsavingWidget, self).__init__(*args, **kwargs)

class Paymentreasonwidget(ModelSelect2Widget):
    search_fields = [
        "client__full_name__icontains",
        "client__phone1__icontains",
        "client__phone2__icontains",
        "client__id_number__icontains",
    ]

    def __init__(self, *args, **kwargs):
        kwargs["data_view"] = "reason-autocomplete"
        super(Paymentreasonwidget, self).__init__(*args, **kwargs)


class StaffWidget(ModelSelect2Widget):
    search_fields = [
        "username__icontains",
        "first_name__icontains",
        "last_name__icontains",
    ]

    def __init__(self, *args, **kwargs):
        kwargs["data_view"] = "staff-autocomplete"
        super(StaffWidget, self).__init__(*args, **kwargs)


class Loancreationform(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            "client",
            "staff",
            "lending_date",
            "loan_amount",
            "interest_rate",
            "registration",
            "period_in_months",
            "payment_plan",
            "notes",
        )
        widgets = {
            "lending_date": DateTimePickerInput(),
            "client": ClientWidget,
             "loan_amount":forms.NumberInput(attrs={'class':'form-control'}),
            "interest_rate":forms.NumberInput(attrs={'class':'form-control'}),
            "period_in_months":forms.NumberInput(attrs={'class':'form-control'}),
            "registration":forms.NumberInput(attrs={'class':'form-control'}),
            "payment_plan":forms.Select(attrs={'class':'form-control'}),
           
            
          
        }
        labels = {
            "client": "Search client by Id/phone",
            "staff": "Select loan officer",
           
        
        }

    def __init__(self, *args, **kwargs):
        super(Loancreationform, self).__init__(*args, **kwargs)
       
        self.fields['client'].required = True
        
        
class Loaneditform(forms.ModelForm):
    class Meta:
        model = Transaction

        fields = (
            "client",
            "staff",
            "lending_date",
            "loan_amount",
            "interest_rate",
            "registration",
            "period_in_months",
            "payment_plan",
            "notes",
            'arrears'
            
        )
        widgets = {
            "lending_date": DateTimePickerInput(),
            "client": ClientWidget,
            
        }
        labels = {
            "client": "Search client by name/phone",
           "staff": "Select loan officer",
            "lending_date": "Lending date",
          
        }

    def __init__(self, *args, **kwargs):
        super(Loaneditform, self).__init__(*args, **kwargs)
   

        self.fields["lending_date"].help_text = "month/date/year"
        self.fields['client'].required = True
        
        


class Clientcreationform(forms.ModelForm):
    class Meta:
        model = Client

        fields = (
            "full_name",
            "id_number",
            "phone1",
            "phone2",
         
            "employer_or_business_type",
            "location",
            "employers_phone",
            "id_front",
            "id_back",
        )
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "id_number": forms.TextInput(attrs={"class": "form-control"}),
            "phone1": forms.TextInput(attrs={"class": "form-control"}),
            "phone2": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "employer_or_business_type": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "employers_phone": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "id_front": forms.FileInput(attrs={"class": "form-control"}),
            "id_back": forms.FileInput(attrs={"class": "form-control"}),
            
        }

    def __init__(self, *args, **kwargs):
        super(Clientcreationform, self).__init__(*args, **kwargs)


class Clientupdateform(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            "full_name",
            "id_number",
            "phone1",
            "phone2",
   
            "employer_or_business_type",
            "location",
            "employers_phone",
            "id_front",
            "id_back",
        )

    def __init__(self, *args, **kwargs):
        super(Clientupdateform, self).__init__(*args, **kwargs)



class Addpaymentform(forms.ModelForm):
    class Meta:
        model = Payment

        fields = (
            "transaction",
            "payment_date",
            "TransAmount",
            "payment_reason",
            "mode_of_payment",
            'notes',
          
          )
        widgets = {
            "transaction": ClientloanWidget,
              "payment_date": DateTimePickerInput(),
            "TransAmount": forms.TextInput(attrs={"class": "form-control"}),
      
            "mode_of_payment": forms.Select(attrs={"class": "form-control"}),
            "payment_reason": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "TransAmount": "Amount",
            "arrear_increment": "Arrears",
        }

    def __init__(self, *args, **kwargs):
        super(Addpaymentform, self).__init__(*args, **kwargs)
       
        self.fields["transaction"].help_text = "Search client  before anything else."
        self.fields['transaction'].required = True
        


class Paymenteditform(forms.ModelForm):
    class Meta:
        model = Payment
        fields = (
            "transaction",
            "payment_date",
            
            "TransAmount",
         
            "payment_reason",
            'notes',
        )
        widgets = {
            "transaction": ClientloanWidget,
            "payment_date": DateTimePickerInput(),
        }
        labels = {
            "TransAmount": "Repayment amount",
     
            "payment_reason": "description",
        }

    def __init__(self, *args, **kwargs):
        super(Paymenteditform, self).__init__(*args, **kwargs)
        self.fields["transaction"].help_text = "Search client  before anything else."
        self.fields['transaction'].required = True
        
class Addexpenseform(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            "lending_date",
            "expense_amount",
            "category",
            "mode_of_payment",
            
            
        )
        widgets = {
            "lending_date": DateTimePickerInput(),
           
            "expense_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "mode_of_payment": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
           
        }
        labels = {
            "lending_date": "Transaction date",
        }

    def __init__(self, *args, **kwargs):
        super(Addexpenseform, self).__init__(*args, **kwargs)




class Cashflowform(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            "lending_date",
            "transaction_amount",
            "transaction_description",
            "mode_of_payment",
            "notes",
        )
        widgets = {
            "lending_date": DateTimePickerInput(),
        }
        labels = {
            "lending_date": "transaction date",
        }

    def __init__(self, *args, **kwargs):
        super(Cashflowform, self).__init__(*args, **kwargs)


