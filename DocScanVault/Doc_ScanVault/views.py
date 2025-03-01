from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Temporarily exempt CSRF protection for simplicity
def index(request):
    if request.method == "GET":
        return render(request, 'Doc_ScanVault/index.html')
    if request.method == "POST":
        print(request.POST.get("Username"))
        print(request.POST.get("Password"))
        try:
            user = User.objects.create(
                Username=request.POST.get('Username'),
                email='lucifer@comp.com',  # Static email for now
                Passwords=make_password(request.POST.get('Password')),  # Hashing the password
                role='User'
            )
            return JsonResponse({'message': 'User created successfully', 'user_id': user.User_id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt  # Temporarily exempt CSRF protection for simplicity
def login(request):
    if request.method == "GET":
        return render(request, 'Doc_ScanVault/login.html')
    if request.method == "POST":
        try:
            username = request.POST.get('Username')
            password = request.POST.get('Password')
            user = User.objects.get(Username=username)
            
            # Debug: Print out password comparison (hashed vs inputted password)
            print(f"Stored Password: {user.Passwords}")
            print(f"Entered Password: {password}")
            
            if check_password(password, user.Passwords):
                return JsonResponse({'message': 'User logged in successfully', 'user_id': user.User_id}, status=200)
            else:
                return JsonResponse({'error': 'Invalid password'}, status=401)
        except User.DoesNotExist:
            # Catch case where user doesn't exist
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
