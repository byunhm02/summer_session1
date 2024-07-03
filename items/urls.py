from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.item),
    path('<int:id>',views.item_detail)
]
