import time

import requests
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django_daraja.mpesa.core import MpesaClient
from rest_framework import generics
from rest_framework.response import Response

from jobs.models import Job
from .models import Transaction, MpesaPaymentResponse
from .serializers import TransactionSerializer, MpesaPaymentResponseSerializer

consumer_key = "8TxXhoqvPvZVGDpTmXYNUEs6GzlEFBQC"
consumer_secret = "YV1fAcp5DSXnXbpk"
shortcode = 174379
pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
checkout_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
transaction_status_url = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"


class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def post(self, request, job_id):
        cl = MpesaClient()
        job = get_object_or_404(Job, id=job_id)
        phone_number = job.phone_number
        amount = int(job.amount)
        reference = "account_reference"  # Update with desired value
        description = "description"  # Update with desired value
        callback_url = "https://willieilus.pythonanywhere.com/pay/callback"
        response = cl.stk_push(phone_number, amount, reference, description, callback_url)

        payment_response = MpesaPaymentResponse.objects.create(
            merchant_request_id=response.merchant_request_id,
            checkout_request_id=response.checkout_request_id,
            response_code=response.response_code,
            response_description=response.response_description,
            customer_message=response.customer_message
        )

        if response.response_code == "0":  # Assuming response.response_code indicates success
            status = "0"  # Change to 0 if it represents the desired status value
        else:
            status = "1"  # Set the default status if the response indicates failure

        time.sleep(15)  # Pause execution for 15 seconds
        transaction = Transaction.objects.create(
            phone_number=phone_number,
            checkout_request_id=payment_response.checkout_request_id,
            reference=reference,
            description=description,
            amount=amount,
            status=status,
            receipt_no=payment_response.checkout_request_id
        )
        return redirect("payments:payment-response-create", checkout_request_id=payment_response.checkout_request_id)


class TransactionDetailView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class MpesaPaymentResponseListView(generics.ListAPIView):
    queryset = MpesaPaymentResponse.objects.all()
    serializer_class = MpesaPaymentResponseSerializer


class MpesaPaymentResponseCreateView(generics.CreateAPIView):
    queryset = MpesaPaymentResponse.objects.all()
    serializer_class = MpesaPaymentResponseSerializer

    def post(self, request, checkout_request_id):
        cl = MpesaClient()
        access_token = cl.access_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token
        }

        payload = {
            "BusinessShortCode": "174379",
            "Password": "MTc0Mzc5YmZiMjc5TliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",
            "Timestamp": "20160216165627",
            "CheckoutRequestID": checkout_request_id,
        }

        response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query', headers=headers,
                                 json=payload)

        result = response.json()
        result_code = result.get('ResultCode')
        result_desc = result.get('ResultDesc')

        payment_response = MpesaPaymentResponse.objects.create(
            response_code=result.get('ResponseCode'),
            response_description=result.get('ResponseDescription'),
            merchant_request_id=result.get('MerchantRequestID'),
            checkout_request_id=result.get('CheckoutRequestID'),
            result_code=result_code,
            result_description=result_desc
        )

        if result_code == "0":
            result_text = "Success: " + result_desc
        else:
            result_text = "Error: " + result_desc

        return Response(result_text)


class MpesaPaymentResponseDetailView(generics.RetrieveAPIView):
    queryset = MpesaPaymentResponse.objects.all()
    serializer_class = MpesaPaymentResponseSerializer
