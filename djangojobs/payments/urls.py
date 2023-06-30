from django.urls import path

from .views import (
    TransactionListView,
    TransactionCreateView,
    TransactionDetailView,
    MpesaPaymentResponseListView,
    MpesaPaymentResponseCreateView,
    MpesaPaymentResponseDetailView,
)

app_name = 'payments'

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/create/<int:job_id>/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('payment-responses/', MpesaPaymentResponseListView.as_view(), name='payment-response-list'),
    path('payment-responses/create/<str:checkout_request_id>/', MpesaPaymentResponseCreateView.as_view(),
         name='payment-response-create'),
    path('payment-responses/<int:pk>/', MpesaPaymentResponseDetailView.as_view(), name='payment-response-detail'),

]
