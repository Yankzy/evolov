from statistics import mode
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json
from . import models


@csrf_exempt
def stripe_webhook(request):
        djson_data = json.loads(request.body.decode('utf-8'))
        print(djson_data)
        return JsonResponse({'accepted': True})
    # data = json.loads(request.body)['data']['object']

    # try:
    
    #     transaction = models.StripeTransaction.objects.get(stripe_transaction_id=data['payment_link'])

    #     if data['payment_status'] == 'paid':
    #         transaction.paid = True
    #         transaction.hook_dump = data
    #         transaction.save()

    #     return JsonResponse({'accepted': True})
    
    # except models.StripeTransaction.DoesNotExist:
        # return JsonResponse({'error': 'transaction not found'}, status=404)
