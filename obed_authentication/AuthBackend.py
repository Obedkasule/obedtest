return render_to_response('sign_and_auth/phone_code.html',{'usercode':user_code, 'u_email':userObj.email_address})
class AuthBackend:
	def aunthenticate(self, request, username=None,password=None):
			try:
				user_instance = UserInfo.objects.get(email=username,pk=password)
				
			except User.DoesNotExist:
				return render_to_response('login.html', {'errorMessage': "Wrong Username or password"})

			uphone_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))

	#==========================sending code to phone number= using nexmo=============================
			client = nexmo.Client(key='1fc5283b', secret='7IAiZBCm8kjM5BsT')
			client.send_message({
		    'from': 'Obed App test',
		    'to': reg_userObj.telephoneNumber,
		    'text': phone_code,
			})

			return render_to_response('code_verify',{'usercode':phone_code,'page':'login'})


	def get_user(self, ):