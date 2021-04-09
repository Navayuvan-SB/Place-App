from django.shortcuts import render
from django.views import generic

from .models import Place


class PlaceListView(generic.ListView):
    model = Place


class PlaceDetailView(generic.DetailView):
    model = Place
