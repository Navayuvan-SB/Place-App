from django.contrib.gis import forms
from django.forms import modelformset_factory

from .models import Place, PlaceType


class PlaceModelForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ("title", "description", "location", "address", "city", "phone")
        widgets = {
            "location": forms.OSMWidget(attrs={"map_width": 800, "map_height": 500})
        }

PlaceTypeFormSet = modelformset_factory(
    PlaceType,
    fields=("place_type",),
    extra=2,
    widgets={"place_type": forms.TextInput(attrs={"placeholder": "Eg. Tourism"})},
)