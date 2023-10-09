from django.urls import path
from .views import (
    PasswordsChangeView,
    Editprofile,
    Profile,
    Staffview,
    make_user_admin,
    make_user_not_admin,
    make_user_not_staff,
    make_user_staff,
    deactivate_user,
    activate_user,
    Editprofile,
    make_user_a_client,
    make_user_not_client,
    can_approve_loan,
    cannot_approve_loan,
    signup,
    Searchstaff,
    Subscription,
    Staffcreation,
)


from django.contrib.auth import views as auth_views


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("add-staff/", Staffcreation, name="create-staff"),

    path("staffs/", Staffview.as_view(), name="staff-home"),
    path("make-user-admin/", make_user_admin, name="make-user-admin"),
    path("make-user-not-admin/", make_user_not_admin, name="make-user-not-admin"),
    path("make-user-staff/", make_user_staff, name="make-user-staff"),
    path("make-user-not-staff/", make_user_not_staff, name="make-user-not-staff"),
    path("make-user-client/", make_user_a_client, name="make-user-client"),
    path("make-user-not-client/", make_user_not_client, name="make-user-not-client"),
    path("can-appprove/", can_approve_loan, name="can-approve"),
    path("cannot-appprove/", cannot_approve_loan, name="cannot-approve"),
    path("search-staff/", Searchstaff.as_view(), name="search-staff"),
    path("activate/", activate_user, name="activate"),
    path("deactivate/", deactivate_user, name="deactivate"),
    path("subscription/", Subscription.as_view(), name="subscription"),

    path("edit-profile/<int:pk>", Editprofile.as_view(), name="edit-profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),
    path(
        "password/",
        PasswordsChangeView.as_view(template_name="accounts/change-password.html"),
        name="change-password",
    ),
    path("edit-profile/", Editprofile.as_view(), name="edit-profile"),
    path("profile/", Profile.as_view(), name="profile"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
