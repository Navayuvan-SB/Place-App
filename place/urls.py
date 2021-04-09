from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlaceListView.as_view(), name='places'),
    path('<int:pk>', views.PlaceDetailView.as_view(), name='place-detail')
]
