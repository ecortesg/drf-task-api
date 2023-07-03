from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer 
from django.db.models import Q


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Tasks': '/tasks/?status=<str:status>&deadline=<str:deadline>', # /tasks/?status=Pendiente&deadline=2023-07-03
        'Create Task': '/task-create/',
        'Update Task As Supervisor': '/supervisor-update/<int:task_id>/',
        'Update Task As Owner': '/owner-update/<int:task_id>/'
    }
    return Response(api_urls)

@api_view(['GET'])
def tasks(request):
    user = request.user
    status = request.query_params.get('status')
    deadline = request.query_params.get('deadline')
    tasks = Task.objects.filter(Q(owner=user) | Q(supervisor=user))
    if status:
        tasks = tasks.filter(status=status)
    if deadline:
        tasks = tasks.filter(deadline=deadline)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def task_create(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PATCH'])
def supervisor_update(request, task_id):
    task = Task.objects.get(pk=task_id)
    
    if request.user != task.supervisor:
        return Response({"error": {"code": 403, "message":"No eres el supervisor de esta tarea"}}, 403)
    
    new_status = request.data.get("status")

    if new_status not in ["Aprobada", "Rechazada"]:
        return Response({"error": {"code": 400, "message":"Como supervisor de esta tarea, únicamente puedes cambiar su estado a 'Aprobada' o 'Rechazada'"}}, 400)

    serializer = TaskSerializer(instance=task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PATCH'])
def owner_update(request, task_id):
    task = Task.objects.get(pk=task_id)
    
    if request.user != task.owner:
        return Response({"error": {"code": 403, "message":"No eres el responsable de esta tarea"}}, 403)
    
    new_status = request.data.get("status")

    if new_status not in ["Pendiente", "Atrasada", "En Proceso", "En Revisión"]:
        return Response({"error": {"code": 400, "message":"Como responsable de esta tarea, únicamente puedes cambiar su estado a 'Pendiente', 'Atrasada', 'En Proceso' o 'En Revisión'"}}, 400)

    serializer = TaskSerializer(instance=task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
