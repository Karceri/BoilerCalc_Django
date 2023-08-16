from django.urls import path
from . import views

# app_name = 'infosystem'

urlpatterns = [
    path('', views.main),
]
