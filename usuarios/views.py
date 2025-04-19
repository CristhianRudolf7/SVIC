from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('usuarios:login')

def custom_login(request):
    if request.method == 'POST':
        dni = request.POST['dni']
        password = request.POST['password']
        user = authenticate(request, dni=dni, password=password)
        
        if user is not None:
            login(request, user)
            if user.rol == 1:
                return redirect('ceo:home')
            elif user.rol == 2:
                return redirect('administrador:home')
            elif user.rol == 3:
                return redirect('ventas:home')
            elif user.rol == 4:
                return redirect('inventario:home')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')