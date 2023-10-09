from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from accounts.models import Account
from .forms import UserCreationForm, UserEditForm,AdminUserCreationForm
from django.views import generic
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict


class PasswordsChangeView(PasswordChangeView):
    success_url = reverse_lazy("staff-home")
    from_class = PasswordChangeForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Account created,you can login")
            return redirect("login")

    else:
        form = UserCreationForm()
  
    return render(request, "accounts/signup.html", {"form": form})
   


def Staffcreation(request):
    if request.method == "POST":
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Staff created successfully")
            return redirect("staff-home")

    else:
        form = AdminUserCreationForm
  
    return render(request, "accounts/staff-signup.html", {"form": form})


class Editprofile(generic.UpdateView):
    form_class = UserEditForm
    template_name = "accounts/edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user


class Profile(LoginRequiredMixin, ListView):
    model = Account
    template_name = "accounts/profiles.html"
    context_object_name = "profiles"


class Staffview(LoginRequiredMixin, ListView):
    queryset = Account.objects.filter(is_superuser=False)
    template_name = "accounts/staff.html"
    context_object_name = "staffs"


class Subscription(LoginRequiredMixin, ListView):
    model = Account
    template_name = "accounts/subscription.html"
    context_object_name = "staffs"


class Editprofile(UpdateView, SuccessMessageMixin):
    model = Account
    form_class = UserEditForm
    template_name = "accounts/edit.html"
    success_message = "User updated successfully"
    success_url = reverse_lazy("staff-home")
    context_object_name = "staff"

    def form_valid(self, form):
        return super().form_valid(form)


def make_user_admin(request):
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    activated_ids = q.getlist("ids")
    Account.objects.filter(pk__in=activated_ids).update(is_admin=True)

    staffs = Account.objects.filter(is_superuser=False)
    context = {"staffs": staffs}

    return render(request, "accounts/partials/staff-partial.html", context)


def make_user_not_admin(request):
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    activated_ids = q.getlist("ids")
    Account.objects.filter(pk__in=activated_ids).update(is_admin=False)

    staffs = Account.objects.filter(is_superuser=False)
    context = {"staffs": staffs}

    return render(request, "accounts/partials/staff-partial.html", context)


def make_user_staff(request):
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    activated_ids = q.getlist("ids")
    Account.objects.filter(pk__in=activated_ids).update(is_staff=True)

    staffs = Account.objects.filter(is_superuser=False)
    context = {"staffs": staffs}

    return render(request, "accounts/partials/staff-partial.html", context)


def make_user_not_staff(request):
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    activated_ids = q.getlist("ids")
    Account.objects.filter(pk__in=activated_ids).update(is_staff=False)

    staffs = Account.objects.filter(is_superuser=False)
    context = {"staffs": staffs}

    return render(request, "accounts/partials/staff-partial.html", context)


def make_user_a_client(request):
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    activated_ids = q.getlist("ids")
    Account.objects.filter(pk__in=activated_ids).update(is_client=True)

    staffs = Account.objects.filter(is_superuser=False)
    context = {"staffs": staffs}

    return render(request, "accounts/partials/staff-partial.html", context)


def make_user_not_client(request):
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    activated_ids = q.getlist("ids")
    Account.objects.filter(pk__in=activated_ids).update(is_client=False)

    staffs = Account.objects.filter(is_superuser=False)
    context = {"staffs": staffs}
    return render(request, "accounts/partials/staff-partial.html", context)


def can_approve_loan(request):
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    activated_ids = q.getlist("ids")
    Account.objects.filter(pk__in=activated_ids).update(can_approve=True)

    staffs = Account.objects.filter(is_superuser=False)
    context = {"staffs": staffs}

    return render(request, "accounts/partials/staff-partial.html", context)


def cannot_approve_loan(request):
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    activated_ids = q.getlist("ids")
    Account.objects.filter(pk__in=activated_ids).update(can_approve=False)

    staffs = Account.objects.filter(is_superuser=False)
    context = {"staffs": staffs}
    return render(request, "accounts/partials/staff-partial.html", context)


def activate_user(request):
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    activated_ids = q.getlist("ids")
    Account.objects.filter(pk__in=activated_ids).update(is_active=True)

    staffs = Account.objects.filter(is_superuser=False)
    context = {"staffs": staffs}

    return render(request, "accounts/partials/staff-partial.html", context)


def deactivate_user(request):
    data = request.body.decode("utf-8")
    q = QueryDict(data, mutable=True)
    activated_ids = q.getlist("ids")
    Account.objects.filter(pk__in=activated_ids).update(is_active=False)

    staffs = Account.objects.filter(is_superuser=False)
    context = {"staffs": staffs}

    return render(request, "accounts/partials/staff-partial.html", context)


class Searchstaff(LoginRequiredMixin, View):
    def get(self, request):
        staffs = Account.objects.all()
        search = request.GET.get("search")
        if search:
            staffs = staffs.filter(
                Q(username__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )
        context = {
            "staffs": staffs,
        }
        return render(request, "accounts/partials/staff-partial.html", context)
