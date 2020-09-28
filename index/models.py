from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


# Create your models here.
class Person(User):
    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username}"


class PersonUpdateForm(ModelForm):
    class Meta:
        model = Person
        fields = ['username', 'email', 'first_name', 'last_name', ]
