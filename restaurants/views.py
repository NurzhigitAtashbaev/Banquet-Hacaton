from django.shortcuts import render
from django.views.generic import ListView


class Main(ListView):
    print('Hello ')
