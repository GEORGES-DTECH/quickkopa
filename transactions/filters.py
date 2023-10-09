import django_filters
from django.forms.widgets import TextInput
from django_filters import DateFilter, CharFilter
from .models import Transaction


class Annualfilter(django_filters.FilterSet):

    year = CharFilter(
        field_name="year",
        lookup_expr="icontains",
        widget=TextInput(attrs={"placeholder": "eg 2022"}),
        label="Financial Year",
    )

    class Meta:
        model = Transaction
        fields = ["year"]


class Monthlyfilter(django_filters.FilterSet):

    month_year = CharFilter(
        field_name="month_year",
        lookup_expr="icontains",
        widget=TextInput(attrs={"placeholder": "eg 3/2022"}),
        label="Month/year",
    )

    class Meta:
        model = Transaction
        fields = ["month_year"]
