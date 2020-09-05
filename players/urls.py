from django.urls import path
from . import views

urlpatterns = [
    path("loadInitial", views.loadInitial, name="loadInitial"),
    path("generateCode", views.generateCode, name="generateCode"),
    path("verifyCode", views.verifyCode, name="verifyCode"),
    path('getRosters', views.getRosters, name="getRosters")
]