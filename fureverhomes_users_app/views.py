from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
	return render(request, 'home_page.html')

def create_account(request):
	return render(request, 'create_account_page.html')