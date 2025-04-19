from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def ceo_home(request):
    if request.user.rol != 1:
        return redirect('usuarios:login')
    return render(request, 'home.html')