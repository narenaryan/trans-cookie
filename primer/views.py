from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from primer.models import Prime
from django.db import transaction,IntegrityError
import json 

# Create your views here.
@csrf_exempt
def supply_primes(request):
    if request.method == 'GET':
        return JsonResponse({'response':'prime numbers insert API'})
    if request.method == 'POST':
        primes = json.loads(request.body)['primes']
        #Validating data before inserting
        valid_prime = Prime()
        for number in primes:
            valid_prime.number = number
            try:
                valid_prime.prime_check()
            except Exception:
                message = {'error': {
                    'prime_number': 'The Prime number : %s \
                     is invalid.' % number}}
                return JsonResponse(message)
        #Carefully look for exceptions in real time at inserting
        transaction.set_autocommit(False)
        for number in primes:
            try:
                Prime(number=number).save()
            except IntegrityError:
                # Revert back checkpoint to initial state. It undo all previous insertions
                transaction.rollback()
                message = {'error': {
                    'prime_number': 'This prime number(%s) is already\
                     registered.' % number}}
                return JsonResponse(message)
        # Commit the changes and flush to db
        transaction.commit()
        return JsonResponse({"response":"data successfully stored"})
