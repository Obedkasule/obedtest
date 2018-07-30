from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import hashers
from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from .forms import UserInfoCreationForm
from .models import UserInfo
from datetime import date
import random, string, logging, requests
import nexmo

'''curl -X POST  https://rest.nexmo.com/sms/json \
-d api_key=1fc5283b \
-d api_secret=7IAiZBCm8kjM5BsT \
-d to=256774382726 \
-d from="NEXMO" \
-d text="Hello from Nexmo'''

# Create your views here.

#=========================handling index requests=====================
def index(request):
	return render(request,'app_home.html')

#=========================handling registration of user requests=====================
def registerUser(request):
	register_form = UserInfoCreationForm()
	if request.method == 'POST':
		reg_userObj = UserInfo()
		reg_userObj.uid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
		reg_userObj.first_name = request.POST.get("f_name")
		reg_userObj.last_name = request.POST.get("o_names")
		reg_userObj.email = request.POST.get("email")
		reg_userObj.telephoneNumber = str(request.POST.get("country_code")) + str(request.POST.get("tele"))
		
#generate code for phone verification=======================

		phone_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4)) 

#============save user object into the database======================
		
		try:		
			reg_userObj.save()
		except IntegrityError:
			errorMessage = "Email already exits"
			return render(request, 'register.html', {'reg_form': register_form, 'withError':errorMessage})

		except:
			errorMessage = "Database error: Please try later"
			return render(request, 'register.html', {'reg_form': register_form, 'withError':errorMessage})


#=========sending code to phone number= using nexmo==========
		client = nexmo.Client(key='1fc5283b', secret='7IAiZBCm8kjM5BsT')
		
		try:
			client.send_message({
		    'from': 'Obed App test',
		    'to': reg_userObj.telephoneNumber,
		    'text': phone_code,
			})
		except:
			return render(request, 'register.html', {'reg_form': register_form, 'withError':'Wrong phone number or no Internet connection'})
		

		return render(request, 'code_verify.html',{'usercode':phone_code, 'u_email':reg_userObj.email, 'page':'register'})

#=========================method is get====================================

	else:
		
		return render(request, 'register.html', {'reg_form': register_form})

#=========================handling user signing/log in requests============
def signIn(request):
	return render(request, 'logged.html')


#=========================method for sending emails========================
def sending_emails(s_message,s_list):
    mail_subject = 'App Test'
    recipient_list = s_list
    send_mail_status = send_mail( mail_subject, s_message, settings.EMAIL_HOST_USER, recipient_list )
    return send_mail_status

@csrf_exempt
def registered(requst):
	email_to = []
	user_object = UserInfo.objects.get(email = requst.POST.get("email"))
	email_to.append(requst.POST.get("email"))
	email_to.append("obedapp.test@gmail.com")
	user_object.set_password(user_object.uid)
	user_object.save()

	#====URL and password============
	message_sent = 'use the url to login: URL\n'+'Your password is: '+user_object.uid
	send_status = sending_emails(message_sent,email_to)
	return render_to_response('registered.html')


def loggingIn(request):
		try:
			user_instance = UserInfo.objects.get(email = request.POST.get('email_address'))
							
		except UserInfo.DoesNotExist:
			return render(request,'login.html', {'withError': "Wrong Username or password"})

		if hashers.check_password(request.POST.get('pword'), user_instance.password):

			phone_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))

	#==========================sending code to phone number= using nexmo=============================
			client = nexmo.Client(key='1fc5283b', secret='7IAiZBCm8kjM5BsT')
			client.send_message({
		    'from': 'Obed App test',
		    'to': user_instance.telephoneNumber,
		    'text': phone_code,
			})
		else:
			return render(request,'login.html', {'withError': "Wrong password"})

		return render(request,'code_verify.html',{'usercode':phone_code,'page':'login'})

@csrf_exempt
def signIn(request):
		return render_to_response('logged.html')

def loginForm(request):
		return render(request, 'login.html')


