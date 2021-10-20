from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
	if request.method != "POST":
		form = UserCreationForm()
	else:
		form = UserCreationForm(data = request.POST)
		if form.is_valid():
			newUser = form.save()
			login(request, newUser)
			return redirect("forum:index")
	context = {
		"form": form
	}
	return render(request, "registration/register.html", context)
