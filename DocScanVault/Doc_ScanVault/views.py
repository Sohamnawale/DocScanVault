import hashlib
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import CreditRequest, Document, ScanTransaction, User, Credit
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils import timezone
import os
from django.conf import settings

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
            credit = Credit.objects.create(user_id = user.User_id, balance = 20, last_reset_date =timezone.now())
            return redirect('login') 
            #return JsonResponse({'message': 'User created successfully', 'user_id': user.User_id}, status=201)
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
                return redirect('user_profile', user_id=user.User_id) #redirect to profile 
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
        return render(request, 'Doc_ScanVault/profile.html',{'user': user,'credit':credit,'user_id': user_id})
    
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

    
def upload(request, user_id):
    user = get_object_or_404(User, User_id=user_id) #get user object
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for uploaded_file in files:
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Calculate content hash
            with open(file_path, 'rb') as f:
                content_hash = hashlib.sha256(f.read()).hexdigest()

            # Save Document
            document = Document.objects.create(
                user_id=user_id,
                title=uploaded_file.name,
                content="Content not stored in db", # or read file and put content, or remove this field.
                file_path=file_path,
                file_size=uploaded_file.size,
                upload_date=timezone.now(),
                content_hash=content_hash,
            )

            # Deduct Credits
            credit = get_object_or_404(Credit, user_id=user_id)
            if credit.balance >= 1:
                credit.balance -= 1
                credit.save()

                # Create Scan Transaction
                ScanTransaction.objects.create(
                    user_id=user_id,
                    document_id=document.document_id,
                    scan_date=timezone.now(),
                    credits_used=1,
                )
            else:
                # Handle insufficient credits (e.g., display an error message)
                return render(request, 'Doc_ScanVault/upload.html', {'error': 'Insufficient credits', 'user_id': user_id})

        return redirect('user_profile', user_id=user_id) #redirect to profile page after upload.

    return render(request, 'Doc_ScanVault/upload.html', {'user_id': user_id})
        
    

