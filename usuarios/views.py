from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .forms import NegocioForm, CustomUserCreationForm, UsuarioProfileForm
from .models import Negocios, Usuarios

# @login_required (o un permiso más específico para quien pueda crear negocios y usuarios)
def crear_negocio_y_usuario_inicial(request):
    if request.method == 'POST':
        negocio_form = NegocioForm(request.POST, request.FILES, prefix="negocio")
        user_form = CustomUserCreationForm(request.POST, prefix="user")
        # El perfil no se puede validar completamente sin el user y negocio_id,
        # pero podemos instanciarlo para pasarlo al template en caso de error inicial.
        # La instancia del perfil se creará después.
        
        # Validar primero el negocio
        if negocio_form.is_valid():
            # Luego validar el usuario (auth.User)
            if user_form.is_valid():
                try:
                    with transaction.atomic(): # Asegura que todas las operaciones se completen o ninguna
                        # 1. Guardar el negocio
                        negocio_instance = negocio_form.save()

                        # 2. Guardar el usuario de Django (auth.User)
                        django_user = user_form.save()
                        # Aquí podrías añadir al usuario a un grupo, etc.

                        # 3. Crear y guardar el perfil de Usuario
                        # Preparamos los datos para UsuarioProfileForm
                        profile_data = {
                            'nombre': user_form.cleaned_data.get('first_name'), # Usar first_name para el perfil
                            'apellido': user_form.cleaned_data.get('last_name'), # Usar last_name para el perfil
                            # Copia otros campos relevantes del POST si es necesario,
                            # o ten campos separados en tu HTML para el perfil.
                            # Por simplicidad, asumimos que algunos campos del perfil
                            # se toman de user_form o se especifican directamente.
                            'dni': request.POST.get('profile-dni'), # Necesitarías un campo 'profile-dni'
                            'rol': 'Gerente', # Asignar rol por defecto
                            'estado': 'Activo',
                            # 'telefono_profile': request.POST.get('profile-telefono'), # Si tienes un campo específico
                        }
                        # Si tienes campos de foto o teléfono específicos para el perfil en el POST
                        # deberás pasarlos aquí también, posiblemente usando un prefijo para el ProfileForm.
                        # Ejemplo, si UsuarioProfileForm también tiene prefijo "profile" en el HTML:
                        # profile_form = UsuarioProfileForm(request.POST, request.FILES, prefix="profile")
                        # PERO, negocio_id y user deben asignarse:

                        # Por ahora, creamos la instancia directamente (simplificado):
                        usuario_profile = Usuarios.objects.create(
                            user=django_user,
                            negocio_id=negocio_instance,
                            nombre=user_form.cleaned_data.get('first_name'), # O de un campo específico del perfil
                            apellido=user_form.cleaned_data.get('last_name'), # O de un campo específico del perfil
                            # Los demás campos como dni, rol, telefono, foto, estado
                            # necesitarían ser recopilados del request.POST
                            # o tener valores por defecto si no se proporcionan.
                            # Ejemplo DNI:
                            # dni = request.POST.get('usuario_dni_field_name') # Reemplaza con el name real
                            # Si usas UsuarioProfileForm para validar estos campos adicionales:
                            # profile_form_data = {k.replace('profile-', ''): v for k,v in request.POST.items() if k.startswith('profile-')}
                            # profile_form_data['negocio_id'] = negocio_instance.negocio_id
                            # profile_form = UsuarioProfileForm(profile_form_data, request.FILES) # Podrías necesitar un prefijo para Files también
                            # if profile_form.is_valid():
                            #    profile = profile_form.save(commit=False)
                            #    profile.user = django_user
                            #    # profile.negocio_id ya estaría seteado por el form si se pasó en data
                            #    profile.save()
                            # else:
                            #    # Manejar error del profile_form, revertir transacción o mostrar errores
                            #    # Esto se vuelve complejo rápidamente, considera un formset o un wizard.

                        )
                        # Aquí puedes añadir una validación y guardado más robusto del UsuarioProfileForm
                        # extrayendo los datos del request.POST (quizás con un prefijo diferente)
                        # y luego asignando `user` y `negocio_id`.

                        messages.success(request, f"Negocio '{negocio_instance.nombre}' y usuario '{django_user.username}' creados exitosamente.")
                        return redirect('alguna_url_de_exito') # Cambia esto

                except Exception as e: # Captura cualquier error durante la transacción
                    messages.error(request, f"Error al crear: {e}")
                    # Los formularios mantendrán los datos ingresados si no se recargan.
            else:
                messages.error(request, "Por favor corrige los errores en el formulario de usuario.")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario de negocio.")
            # Si el user_form también tuvo errores, se mostrarán.
            if not user_form.is_valid():
                 messages.error(request, "Por favor corrige también los errores en el formulario de usuario.")


        # Si llegamos aquí, algo falló, re-renderizar con los forms y errores.
        # Necesitas instanciar el profile_form aquí también si quieres mostrar sus errores
        # profile_form = UsuarioProfileForm(request.POST, request.FILES, prefix="profile")
        # if not profile_form.is_valid():
        #     pass # Los errores se mostrarán en el template

    else: # Método GET
        negocio_form = NegocioForm(prefix="negocio")
        user_form = CustomUserCreationForm(prefix="user")
        # profile_form = UsuarioProfileForm(prefix="profile") # Para campos del perfil separados

    context = {
        'negocio_form': negocio_form,
        'user_form': user_form,
        # 'profile_form': profile_form, # Si usas un form separado para el perfil en el template
        'titulo_pagina': "Crear Nuevo Negocio y Usuario Gerente"
    }
    return render(request, 'tu_template_creacion.html', context)

# Para crear solo un usuario para un negocio existente:
# @login_required
def crear_usuario_para_negocio(request, negocio_id_param): # negocio_id vendría de la URL
    try:
        negocio = Negocios.objects.get(pk=negocio_id_param)
    except Negocios.DoesNotExist:
        messages.error(request, "El negocio especificado no existe.")
        return redirect('alguna_url_de_error_o_lista_negocios')

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, prefix="user")
        profile_form = UsuarioProfileForm(request.POST, request.FILES, prefix="profile")

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    django_user = user_form.save()
                    
                    # Crear el perfil
                    usuario_profile = profile_form.save(commit=False)
                    usuario_profile.user = django_user
                    usuario_profile.negocio_id = negocio # Asignar el negocio existente
                    # Asegurarse que nombre y apellido del perfil coincidan con el user si así se desea
                    # o que se hayan llenado correctamente en el profile_form
                    if not profile_form.cleaned_data.get('nombre'): # Si no se llenó específicamente
                        usuario_profile.nombre = django_user.first_name
                    if not profile_form.cleaned_data.get('apellido'):
                        usuario_profile.apellido = django_user.last_name

                    usuario_profile.save()
                    
                    messages.success(request, f"Usuario '{django_user.username}' creado para el negocio '{negocio.nombre}'.")
                    return redirect('alguna_url_de_exito_usuarios', negocio_id=negocio.pk) # ej: a la lista de usuarios del negocio
            except Exception as e:
                messages.error(request, f"Error al crear el usuario: {e}")
        else:
            messages.error(request, "Por favor corrige los errores en los formularios.")
    else:
        user_form = CustomUserCreationForm(prefix="user")
        profile_form = UsuarioProfileForm(prefix="profile", initial={'negocio_id': negocio})
        # Puedes pre-rellenar el negocio_id si es un campo visible y editable,
        # o simplemente pasarlo al guardar. Si el campo 'negocio_id' en UsuarioProfileForm
        # está deshabilitado o no se muestra, asegúrate de asignarlo antes de `profile_form.save()`.

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'negocio': negocio,
        'titulo_pagina': f"Crear Usuario para {negocio.nombre}"
    }
    return render(request, 'tu_template_crear_usuario.html', context)

def landing(request):
    return render(request, 'landingCuerpo.html')

def registro(request):
    return render(request, 'IniciarSesion.html')

def crearEmpresa(request):
    return render(request, 'crearCuenta.html')