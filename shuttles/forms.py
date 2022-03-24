from django.forms import ModelForm
from shuttles.models import *


class ShuttleForm(ModelForm):
    class Meta:
        model = Shuttle
        fields = "__all__"
        exclude = ["organization", "id_number", "added_at"]
