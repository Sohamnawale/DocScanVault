from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
import os
from django.conf import settings
from django.http import JsonResponse
from PIL import Image

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, 'Doc_ScanVault/index.html')