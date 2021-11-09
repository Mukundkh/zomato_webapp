from django.shortcuts import render
from .models import restaurant_model
# Create your views here.
print(restaurant_model.objects.all())