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


def edit_place_view(request, pk):
    template_name = "place/place_form.html"

    if request.method == "GET":

        place = Place.objects.get(pk=pk)
        place_types = place.placetype_set.all()

        place_form = PlaceModelForm(instance=place)
        formset = PlaceTypeFormSet(queryset=place_types)

    elif request.method == "POST":
        place = Place.objects.get(pk=pk)
        old_place_types = place.placetype_set.all()

        place_form = PlaceModelForm(request.POST, instance=place)
        formset = PlaceTypeFormSet(request.POST, queryset=old_place_types)

        if place_form.is_valid() and formset.is_valid():
            new_place = place_form.save()

            update_deleted_place_type(old_place_types, formset)

            for form in formset:
                new_place_type = form.save(commit=False)

                if isPlaceTypeEmpty(new_place_type):
                    continue

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


def isPlaceTypeEmpty(new_place_type):
    return str(new_place_type.place_type).strip() == ""


def update_deleted_place_type(old_place_types, formset):

    for old_place_type in old_place_types:
        is_deleted = False
        for form_cleaned_data in formset.cleaned_data:

            if form_cleaned_data["id"] == old_place_type:
                break

            elif (
                form_cleaned_data["id"] != old_place_type
                and form_cleaned_data["id"] is not None
            ):
                is_deleted = True

        if is_deleted:
            old_place_type.delete()