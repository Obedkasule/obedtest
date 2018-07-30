from django import forms


class UserInfoCreationForm(forms.Form):

	countries = [('','Country'),('+1', 'USA'),('+256','Uganda'),('+2','Canada')]
	first_name = forms.CharField(max_length=15)
	other_names = forms.CharField(max_length=30)
	email = forms.CharField(max_length=20)
	country_code = forms.ChoiceField(label = 'Country', widget = forms.Select, choices = countries)
	telephone = forms.CharField(max_length=15)