from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Inspeccionambientes
from django.http import JsonResponse
import openpyxl

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



def registrar_inspeccion(request):
    if request.method == "POST":
        # Obtener los datos del formulario
        usuario = request.user
        laboratorio = request.POST.get("ambientes")
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
            laboratorio=laboratorio,
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
    inspecciones = Inspeccionambientes.objects.all()
    return render(request, "read_inspeccion.html", {"inspecciones": inspecciones})






def exportar_inspeccion_con_plantilla(request):
    # Ruta de la plantilla
    template_path = os.path.join(os.path.dirname(__file__), "media", "plantilla.xlsx")
    # Cargar la plantilla
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active  # Usamos la primera hoja

    # Obtener los registros
    inspecciones = Inspeccionambientes.objects.all()

    # Empezar a llenar desde la fila 2 (asumiendo que la fila 1 tiene encabezados)
    fila = 5

    for inspeccion in inspecciones:
    # Asegurarse de escribir solo en celdas no combinadas
        columnas = ["B", "Q", "C", "D", "E", "G", "I", "K", "M", "O","R"]
        valores = [
            inspeccion.id,
            inspeccion.usuario.username,  # Asegúrate de que el campo 'usuario' existe
            inspeccion.fecha_registro.strftime("%Y-%m-%d %H:%M"),
            inspeccion.laboratorio,
            inspeccion.equipo_computo,
            inspeccion.proyector_multimedia,
            inspeccion.red,
            inspeccion.fluido_electrico,
            inspeccion.orden_limpieza,
            inspeccion.modulos,
            inspeccion.observacion
        ]

    for col, valor in zip(columnas, valores):
        cell = ws[f"{col}{fila}"]

        # Verificar si la celda es parte de una combinación
        if any(cell.coordinate in merged_range for merged_range in ws.merged_cells.ranges):
            # Obtener la celda superior izquierda de la combinación
            for merged_range in ws.merged_cells.ranges:
                if cell.coordinate in merged_range:
                    top_left_cell = ws.cell(row=merged_range.min_row, column=merged_range.min_col)
                    top_left_cell.value = valor
                    break
        else:
            cell.value = valor  # Escribir directamente si no está combinada

    fila += 1  # Pasar a la siguiente fila

    # Configurar la respuesta HTTP para la descarga
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="reporte_inspecciones.xlsx"'

    # Guardar el archivo en la respuesta
    wb.save(response)
    return response