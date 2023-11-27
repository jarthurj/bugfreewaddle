from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()
	username =forms.CharField(max_length=50, 
				required=False,
				widget=forms.TextInput(),
				label="Username:")
	class Meta:
		model = User
		fields = ['email','username']