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


class PlaceTypeForm(forms.ModelForm):
    class Meta:
        model = PlaceType
        fields = ("place_type",)
        {
            "place_type": forms.TextInput(
                attrs={"placeholder": "Eg. Tourism", "required": "false"}
            )
        }

    def __init__(self, *args, **kwargs):
        super(PlaceTypeForm, self).__init__(*args, **kwargs)
        self.fields["place_type"].required = False


PlaceTypeFormSet = modelformset_factory(PlaceType, extra=2, form=PlaceTypeForm)
