from django.urls import path
from . import views

urlpatterns = [
    path('customer/<str:phone>/', views.get_customer),
    path('loan/<str:phone>/', views.get_loan),
    path('log/', views.add_log),
    path('loan/update/<str:phone>/', views.update_loan),
    path('chat/<str:phone>/', views.chat_with_ai),
]