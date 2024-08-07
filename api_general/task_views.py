from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from myapp.models import Tarea
from myapp.models import Usuario
from .serializers import TareaSerializer

class TareaListCreateAPIView(APIView):
    def get(self, request):
        tareas = Tarea.objects.all()
        serializer = TareaSerializer(tareas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TareaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TareaRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Tarea, pk=pk)

    def get(self, request, pk):
        tarea = self.get_object(pk)
        serializer = TareaSerializer(tarea)
        return Response(serializer.data)

    def put(self, request, pk):
        tarea = self.get_object(pk)
        user_id = request.data['idUsuario']
        user = Usuario.objects.get(id=user_id)
        serializer = TareaSerializer(tarea, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serialized_user = {
                'nombre':user.nombre,
                'apellido':user.apellido,
                'correo':user.correo,
                'tarea': serializer.data
            }
            return Response(serialized_user)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        tarea = self.get_object(pk)
        serializer = TareaSerializer(tarea, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tarea = self.get_object(pk)
        tarea.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
