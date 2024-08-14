from django.shortcuts import render
from django.views import View

# Create your views here.

class MainPageView(View):
    def get(self, request):
        return render (request, 'shop/main.html')