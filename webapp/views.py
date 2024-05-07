from django.shortcuts import render
from flask import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Patient
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
import requests  # Add this import statement for the requests module

# Create your views here.
GOOGLE_API_KEY='AIzaSyARwRyEByZcvGVbkopD6pa4uqdVrYDNNKQ'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@csrf_exempt
@login_required
def home(req):
    return render(req, 'home.html')

def start(req):
    return render(req, 'start.html')

@csrf_exempt
def index(req):
    return render(req, 'index.html', {})

def pharmacy(req):
    return render(req, 'pharmacy.html', {})

def success(request):
    return render(request, 'success.html')

def logout(request):
    return render(request, 'logout.html')

def blynk_template(request):
    blynk_data = get_blynk_data()  # Fetch data from the Blynk API
    return JsonResponse(blynk_data, safe=False) 

from django.http import HttpResponseRedirect

def redirect_to_blynk(request):
    # URL of the Blynk dashboard
    blynk_url = 'https://blynk.cloud/dashboard/307004/global/devices/2285481/organization/307004/devices/1087223/dashboard'
    return HttpResponseRedirect(blynk_url)


@login_required
def prescription(req):
    data = req.GET['msg']
    EMAIL_ADDRESS = "pharmacy1xyz@gmail.com"
    EMAIL_PASSWORD = "lvzghzuyejporsyw"
    msg = EmailMessage()
    msg['Subject'] = 'Prescription'
    msg['From'] = 'pharmacy1xyz@gmail.com' 
    msg['To'] = 'pharmacy1xyz@gmail.com'

    msg.set_content("""
    <!DOCTYPE html>
    <html>
    <body style="background-color: #e9ecef;">
    <div>
        E-Sanjivini Prescription

        <p> Patient Name : Sample Patient </p>
        <p> Address : No 1, Sample Street Chennai </p>
        <p> Age : 80 </p>
        <p> Gender : Male </p>
        <p> Mobile : 9955995599 </p>
        <p>
        """ + 
        data + """</p>

        <br>
        <br>
        <br>

        <p>Thank you</p>
    </body>
    </html>
    """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
        smtp.send_message(msg)
    
    return render(req, 'prescription.html', {})

@csrf_exempt
def smartcard(req):
    return render(req, 'smartcard.html', {})

# def login(req):
#     return render(req, 'login.html', {})

@csrf_exempt
def auth_login(request):
    context = {}
    
    if request.user.is_authenticated:    
        return redirect('/auth_login')
    else:
        pass

    if request.method == 'POST':
        username = request.POST['emailid'] #username
        password = request.POST['password'] #password
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            print("loggedin")
            return redirect('home')
        else:
            context = {"error":"error"}
            print("error1")
    else:
        print("error2")
    return render(request,'login.html',context)

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["emailid"]
        password = request.POST["password"]      
        user = User.objects.create_user(email, email, password)
        user.first_name = username
        user.is_active = False
        user.save()
    return render(request, 'register.html', {})

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        input_val = request.POST.get('message')  # Assuming 'message' is the key sent in AJAX data
        print("Input value:", input_val)
        req_value = "Give me sample medication for bellow patient message " + input_val
        req_value +=  "Give me only medication in list as 1, 2 ,3 formate also remove all special character"
        response = model.generate_content(req_value)
        print(response.text)
        # Perform any processing here based on the input value
        # Return JSON response
        return JsonResponse({'message': response.text}, status=200)
    else:
        # Handle other HTTP methods or return an error response
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def save_patient_details(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        phone_number = request.POST.get('phone_number')
        aadhar_number = request.POST.get('aadhar_number')
        address = request.POST.get('address')
        state = request.POST.get('state')
        language = request.POST.get('language')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        # Create a new Patient object and save it to the database
        patient = Patient(
            Full_Name=full_name,
            Gender=gender,
            DOB=dob,
            Ph_number=phone_number,
            Aadhar_number=aadhar_number,
            Address=address,
            state=state,
            Language=language,
            city=city,
            postal_code=postal_code
        )
        patient.save()

        return redirect('success')  # Redirect to a success page after saving
    else:
        return render(request, 'error_page.html')  # Handle GET requests

def get_blynk_data():
    url = 'https://blynk.cloud/dashboard/307004/global/devices/2285481/organization/307004/devices/1087223/dashboard'
    headers = {
        'Authorization': 'Bearer yBX15ySyMK1SXl6oaozIBrWq61YW77gb'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        return data
    except requests.RequestException as e:
        print("Request to Blynk API failed:", e)
        print(e)
        return None
    except json.JSONDecodeError as e:
        print("Failed to parse JSON response from Blynk API:", e)
        return None


# Assuming get_blynk_data is defined in the same file or imported

def blynk_view(request):
    blynk_data = get_blynk_data()  # Call the function to get data
    return render(request, 'blynk_template.html', {'blynk_data': blynk_data})
