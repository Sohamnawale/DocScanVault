from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
import os
from django.conf import settings
from django.http import JsonResponse
from PIL import Image
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from .models import User, Document, Log, CreditRequest, Credit, ScanTransaction, DocumentMatch, DocumentMetadata
from django.views.decorators.csrf import csrf_exempt
import json

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, 'Doc_ScanVault/index.html')
    if request.method == "POST":
        print(request.POST.get("Username"))
        print(request.POST.get("Password"))
        try:
            user = User.objects.create(
                Username=request.POST.get['Username'],
                email=request.POST.get['email'],
                Passwords=make_password(request.POST.get['Passwords']),
                role=request.POST.get['role']
            )
            return JsonResponse({'message': 'User created successfully', 'user_id': user.User_id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def login(request):
    if request.method == "GET":
        return render(request, 'Doc_ScanVault/login.html')
    if request.method == "POST":
        try:
            user = User.objects.get(Username=request.POST.get('Username'))
            if check_password(request.POST.get('Password'), user.Passwords):
                return JsonResponse({'message': 'User logged in successfully', 'user_id': user.User_id},
                                    status=200)
            else:
                return JsonResponse({'error': 'Invalid password'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)