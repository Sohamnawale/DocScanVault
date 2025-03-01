from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import CreditRequest, User, Credit
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils import timezone

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
            credit = Credit.objects.create(user_id = user.User_id, balance = 20, last_reset_date =timezone.now()) # 
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
            credit = get_object_or_404(Credit, user_id = user.User_id)
            print(credit.balance)
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

def user_profile(request,user_id):
    if request.method == "GET":
        user = get_object_or_404(User, User_id=user_id)
        credit = get_object_or_404(Credit, user_id=user_id)
        return render(request, 'Doc_ScanVault/profile.html',{'user': user,'credit':credit})
    
    try:
        user = User.objects.get(User_id=user_id)
        credit = Credit.objects.get(user_id=user_id)

        return JsonResponse({
            'user': {
                'id': user.User_id,
                'username': user.Username,
                'email': user.email,
                'role': user.role
            },
            'credits':{
                'balance':credit.balance,
                'last_reset_date': credit.last_reset_date
            }
        },status = 200)
    except User.DoesNotExist:
        return JsonResponse({'error':'User not found'},status = 404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def request_credits(request, user_id):
    """
    POST /credits/request/:user_id
    Request admin to add credits to user account
    """
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    try:
        # Check if user exists
        try:
            user = User.objects.get(User_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        # Get amount from request body
        amount = request.POST.get('amount')
        if not amount:
            return JsonResponse({'error': 'Amount is required'}, status=400)
        
        amount = int(amount)
        if amount <= 0:
            return JsonResponse({'error': 'Amount must be greater than zero'}, status=400)
        
        # Create credit request
        credit_request = CreditRequest.objects.create(
            user_id=user_id,
            amount=amount,
            status=CreditRequest.Status.PENDING,
            requested_at=timezone.now()
        )
        
        return JsonResponse({
            'message': 'Credit request sent to admin',
            'request_id': credit_request.request_id,
            'status': credit_request.status
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


        
    

