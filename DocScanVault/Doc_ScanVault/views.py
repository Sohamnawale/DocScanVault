from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
import os
from django.conf import settings
from django.http import JsonResponse
from PIL import Image
from IPython.display import Markdown
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, 'Doc_ScanVault/index.html')
    if request.method == "POST":
        print(request.POST.get("Username"))
        print(request.POST.get("Password"))
        return JsonResponse({'message': 'User created successfully'}, status=201)
        