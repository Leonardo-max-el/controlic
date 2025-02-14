from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Inspeccionambientes
from django.http import JsonResponse
import openpyxl
from django.core.paginator import Paginator

from django.conf import settings
from openpyxl.utils import get_column_letter
import os


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
                return redirect('registrar_inspeccion')
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

# cambiar el laoratorio por ambientes

def registrar_inspeccion(request):
    if request.method == "POST":
        # Obtener los datos del formulario
        usuario = request.user
        tipo_ambiente = request.POST.get("tipo_ambiente")
        ambiente = request.POST.get("ambiente")
        equipo_computo = request.POST.get("equipo_computo")
        proyector_multimedia = request.POST.get("proyector_multimedia")
        red = request.POST.get("red")
        fluido_electrico = request.POST.get("fluido_electrico")
        orden_limpieza = request.POST.get("orden_limpieza")
        modulos = request.POST.get("modulos")
        
        # Asignar un valor por defecto si `observacion` está vacío o None
        observacion = request.POST.get("observaciones", "").strip()
        if not observacion:
            observacion = "NO SE ENCONTRARON OBSERVACIONES"

        # Guardar en la base de datos
        Inspeccionambientes.objects.create(
            usuario=usuario,

            tipo_ambiente=tipo_ambiente,
            ambiente=ambiente,
  
            equipo_computo=equipo_computo,
            proyector_multimedia=proyector_multimedia,
            red=red,
            fluido_electrico=fluido_electrico,
            orden_limpieza=orden_limpieza,
            modulos=modulos,
            observacion=observacion  # Aseguramos que nunca sea None
        )

        return JsonResponse({"mensaje": "Registro guardado exitosamente"}, status=200)

    return render(request, "registrar_inspeccion.html")




def read_inspeccion(request):
    inspecciones_list = Inspeccionambientes.objects.all()
    paginator = Paginator(inspecciones_list, 5)  # 10 elementos por página
    page_number = request.GET.get('page')
    inspecciones = paginator.get_page(page_number)
    
    return render(request, "read_inspeccion.html", {"inspecciones": inspecciones})


def exportar_inspeccion_con_plantilla(request):
    # Ruta de la plantilla
    template_path = os.path.join(os.path.dirname(__file__), "media", "plantilla.xlsx")
    # Cargar la plantilla
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active  # Usamos la primera hoja

    # Obtener los registros
    inspecciones = Inspeccionambientes.objects.all()

    fila = 11  # Suponiendo que los registros inician en la fila 5

    for inspeccion in inspecciones:
        columnas_fijas = ["D", "E", "R", "S"]  # Columnas fijas (ID, Usuario, Fecha, Laboratorio, Observación)
        valores_fijos = [
            # inspeccion.id,
            inspeccion.tipo_ambiente,
            inspeccion.ambiente,
            # inspeccion.fecha_registro.strftime("%Y-%m-%d %H:%M"),
            inspeccion.usuario.username,  
            inspeccion.observacion
        ]

        # Asignamos los valores fijos (ID, Usuario, Fecha, etc.)
        for col, valor in zip(columnas_fijas, valores_fijos):
            ws[f"{col}{fila}"] = valor

        # Definir los valores y sus respectivas columnas para "C" y "O"
        valores_dinamicos = [
            inspeccion.equipo_computo, 
            inspeccion.proyector_multimedia, 
            inspeccion.red, 
            inspeccion.fluido_electrico, 
            inspeccion.orden_limpieza, 
            inspeccion.modulos
        ]

        # Asignamos "X" en la columna correcta según el valor de cada campo
        for col_c, col_o, valor in zip(["F", "H", "J", "L", "N", "P"], ["G", "I", "K","M","O","Q"], valores_dinamicos):
            if valor == "C":
                ws[f"{col_c}{fila}"] = "X"  # Si es "C", lo pone en su columna
            elif valor == "O":
                ws[f"{col_o}{fila}"] = "X"  # Si es "O", lo pone en su columna correspondiente

        fila += 1  # Pasamos a la siguiente fila


    # Configurar la respuesta HTTP para la descarga
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="reporte_inspecciones.xlsx"'

    # Guardar el archivo en la respuesta
    wb.save(response)
    return response