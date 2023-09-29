# Определение представления (view) для главной страницы
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
