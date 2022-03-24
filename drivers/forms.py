from django.forms import ModelForm
from drivers.models import *


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"
        exclude = ["organization", "id_number", "added_at"]
