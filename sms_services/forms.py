from django import forms
from .models import DeliveryReport, Outbox


class Outboxform(forms.ModelForm):
    class Meta:
        model = Outbox
        fields = (
            "phone_numbers",
            "text_message",
        )

    def __init__(self, staff, *args, **kwargs):

        super(Outboxform, self).__init__(*args, **kwargs)
        self.fields["phone_numbers"].widget.attrs[
            "placeholder"
        ] = "0727574812,0115209562"

