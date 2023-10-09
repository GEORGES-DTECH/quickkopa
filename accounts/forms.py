from .models import Account
from django.contrib.auth.forms import UserCreationForm, UserChangeForm




class UserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",

            "username",
            "password1",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        del self.fields["password2"]

        for fieldname in [
            "first_name",
            "last_name",

            "username",
            "password1",
            "email",
        ]:self.fields[fieldname].help_text = None
           



class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",

            "username",
            "password1",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super(AdminUserCreationForm, self).__init__(*args, **kwargs)
        # del self.fields["password2"]

        for fieldname in [
            "first_name",
            "last_name",

            "username",
            "password1",
            "email",
        ]:self.fields[fieldname].help_text = None
           



class UserEditForm(UserChangeForm):
    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",

            "username",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        for fieldname in [
            "first_name",
            "username",
            "email",
        ]:

            self.fields[fieldname].help_text = None
