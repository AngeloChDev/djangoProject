from django import forms
from django.forms.fields import CharField
from django.core.exceptions import ValidationError
from .models import Teams, Profiles, Players, Games, Gols_Scored


class ADMlogin(forms.Form):
      text_input = forms.CharField(max_length=3)
      password_input = forms.CharField(min_length=8, widget=forms.PasswordInput)



class TeamsModefForm(forms.ModelForm):
      class Meta:
            model = Teams
            fields = "__all__"
            widgets={
                  
                  "name":forms.TextInput(attrs={"class":"form-control fs-3"}),
                  "town":forms.TextInput(attrs={"class":"form-control fs-3"}),
                  "color":forms.TextInput(attrs={"class":"form-control fs-3"}),
            
            }
            