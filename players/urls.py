from django.urls import path
from . import views

urlpatterns = [
    path("loadInitial", views.loadInitial, name="loadInitial")
]