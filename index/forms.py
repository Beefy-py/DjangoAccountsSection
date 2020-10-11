import string

from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Person


class PersonRegisterForm(forms.Form):
    username = forms.CharField(min_length=2, max_length=14, required=True)
    password = forms.CharField(min_length=8, max_length=100, required=True)
    confirm_password = forms.CharField(min_length=8, max_length=100, label='ConfirmPassword')
    email = forms.EmailField(min_length=8, max_length=100, required=True)
    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)

    def clean_username(self):
        cd = self.cleaned_data
        if not cd['username'].isalnum():
            self.add_error('username', f'The username must only contain letter and numbers!')
        if Person.objects.filter(username=cd['username']).exists():
            self.add_error('username', f'That username is already registered!')
        else:
            return cd['username']

    def clean_email(self):
        cd = self.cleaned_data
        if Person.objects.filter(email=cd['email'].lower()).exists():
            self.add_error('email', f'Someone already uses that email!')
        else:
            return cd['email']

    def clean_first_name(self):
        cd = self.cleaned_data
        for i in cd['first_name']:
            if i in string.punctuation:
                self.add_error('first_name', f'FirstName must not contain symbols!')
                return ''
        else:
            return cd['first_name']

    def clean_last_name(self):
        cd = self.cleaned_data
        for i in cd['last_name']:
            if i in string.punctuation:
                self.add_error('last_name', f'LastName must not contain symbols!')
                return ''
        else:
            return cd['last_name']

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            self.add_error('confirm_password', f'The passwords do not match!')
            return ''
        else:
            return cd['confirm_password']


class PersonLoginForm(forms.Form):
    username = forms.CharField(min_length=2, max_length=14, required=True)
    password = forms.CharField(min_length=8, max_length=100, required=True)

    def clean_username(self):
        user = Person.objects.filter(username=self.cleaned_data['username'])
        if not list(user):
            self.add_error('username', f'This username does not exist!')
            return ''
        return self.cleaned_data['username']

    def clean_password(self):
        username = self.cleaned_data['username']
        if not username:
            return ''
        print(username)
        user = Person.objects.get(username=self.cleaned_data['username'])
        if not user.check_password(self.cleaned_data['password']):
            self.add_error('password', f'Inconsistent password for user')
            return ''
        else:
            return self.cleaned_data['password']
