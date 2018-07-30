
from django.urls import path
from . import views


app_name = 'obed_authentication'
urlpatterns = [
    path('', views.index, name='index'), # for index
    path('signUp', views.registerUser, name='register'), # dealing with sign-up information

    path('log', views.signIn, name='sign_in'),#logging in phone code
    path('done_register', views.registered, name='reg_done'),# sign up phone code
    path('logging_in', views.loggingIn, name='login'),
]
