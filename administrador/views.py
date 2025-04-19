from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def home(request):
    if request.user.rol != 2:
        return redirect('usuarios:login')
    return render(request, 'home.html')