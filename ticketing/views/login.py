from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render


def my_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():


    else:
        form = AuthenticationForm()

    return render(request, 'forms/login.html', {'form':form})