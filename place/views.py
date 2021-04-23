from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from extra_views import (
    CreateWithInlinesView,
    UpdateWithInlinesView,
    InlineFormSetFactory,
)
from django.urls import reverse

from .filters import PlaceFilter
from .forms import PlaceModelForm, PlaceTypeFormSet

from django.contrib.gis.geos import Point

from .models import Place, PlaceType


class PlaceListView(generic.ListView):
    model = Place

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = PlaceFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PlaceDetailView(generic.DetailView):
    model = Place


class PlaceTypeInline(InlineFormSetFactory):
    model = PlaceType
    fields = ["place_type"]
    factory_kwargs = {
        "extra": 2,
        "max_num": None,
        "can_order": False,
        "can_delete": False,
    }


def add_place_view(request):
    template_name = "place/place_form.html"

    if request.method == "GET":
        place_form = PlaceModelForm(request.GET or None)
        formset = PlaceTypeFormSet(queryset=PlaceType.objects.none())

    elif request.method == "POST":
        place_form = PlaceModelForm(request.POST)
        formset = PlaceTypeFormSet(request.POST)

        if place_form.is_valid() and formset.is_valid():
            new_place = place_form.save()

            for form in formset:

                new_place_type = form.save(commit=False)
                new_place_type.place = new_place
                new_place_type.save()

            return redirect("place-detail", pk=new_place.pk)

    return render(
        request, template_name, {"place_form": place_form, "formset": formset}
    )


class EditPlaceView(UpdateWithInlinesView):
    # form_class = PlaceForm
    model = Place
    template_name = "place/place_form.html"
    fields = "__all__"
    inlines = [PlaceTypeInline]

    def form_valid(self, form):
        form.instance.location = form.cleaned_data["location"]
        return super(EditPlaceView, self).form_valid(form)

    def get_success_url(self):
        return reverse("places")


class DeletePlaceView(DeleteView):
    model = Place

    def get_success_url(self):
        return reverse("places")
