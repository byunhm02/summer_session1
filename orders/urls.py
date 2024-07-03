from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.order),
    path('<int:id>',views.order_delete_detail)
]