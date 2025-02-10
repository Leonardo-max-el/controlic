from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Inspeccionambientes
from django.http import JsonResponse


# Imortamos el login para poder autenticar al usuario dentro del navegador
from django.contrib.auth import login, logout,authenticate
from django.db import IntegrityError



# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render (request, 'signup.html', {'form': UserCreationForm()})
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('Inspeccion')
                # return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'Usuario creado correctamente'})
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'El usuario ya existe'})
        
        return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'Las contraseñas no coinciden'})
        

def clouses(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login_view.html',{
            'form':AuthenticationForm
    })
    else: 
        user = authenticate(
            request, username=request.POST['username'], 
            password=request.POST['password'])
        
        if user is None:
            return render(request, 'login_view.html',{
                'form':AuthenticationForm,
                'error': 'Usuario o contraseña Incorrecto'
            })
    
        else:
            login(request, user)
            return redirect('registrar_inspeccion')



def registrar_inspeccion(request):
    if request.method == "POST":
        laboratorio = "Laboratorio A"
        equipo_computo = request.POST.get("equipo_computo")
        proyector_multimedia = request.POST.get("proyector_multimedia")
        red = request.POST.get("red")
        fluido_electrico = request.POST.get("fluido_electrico")
        orden_limpieza = request.POST.get("orden_limpieza")
        modulos = request.POST.get("modulos")

        # Guardar en la base de datos
        Inspeccionambientes.objects.create(
            laboratorio=laboratorio,
            equipo_computo=equipo_computo,
            proyector_multimedia=proyector_multimedia,
            red=red,
            fluido_electrico=fluido_electrico,
            orden_limpieza=orden_limpieza,
            modulos=modulos
        )

        return JsonResponse({"mensaje": "Registro guardado exitosamente"}, status=200)

    return render(request, "inspeccion.html") 