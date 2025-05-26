from django.shortcuts import render, redirect
from .forms import CrearUsuarioForm

def register(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    else:
        form = CrearUsuarioForm()

    return render(request, 'accounts/register.html', {'form': form})