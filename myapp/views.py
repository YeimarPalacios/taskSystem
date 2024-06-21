from django.shortcuts import render

def example_view(request):
    return render(request, 'miapp/example.html')

def login_view(request):
    return render(request, 'miapp/login.html')

def menu_view(request):
    return render(request, 'miapp/menu.html')

def panel_view(request):
    return render(request, 'miapp/panel.html')

def registro_view(request):
    return render(request, 'miapp/registro.html')

def task_item_view(request, tarea_id):
    # Aquí puedes incluir lógica para obtener detalles de la tarea con el ID tarea_id
    # Por ejemplo:
    # tarea = Tarea.objects.get(pk=tarea_id)
    # return render(request, 'miapp/task_item.html', {'tarea': tarea})
    return render(request, 'miapp/task_item.html', {'tarea_id': tarea_id})