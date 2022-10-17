from django.shortcuts import render
from .forms import CreateAccount
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def home(request):
	return render(request, 'home_page.html')

def create_account(request):
	if request.method == 'POST':
		form = CreateAccount(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('successfully created new account')
		else:
			return render(request, 'create_account_page.html')


