from django.test import TestCase
from models import Teams


d={'HSVz':{'name':'HSV', 'town':'Hamburg(DE)', 'color':'Blue'}}
# Create your tests here.
t = Teams.objects.create(**d['HSVz'])