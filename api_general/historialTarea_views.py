from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from myapp.models import HistorialTarea
from .serializers import HistorialTareaSerializer

class HistorialTareaListCreateAPIView(APIView):
    def get(self, request):
        historial_tareas = HistorialTarea.objects.all()
        serializer = HistorialTareaSerializer(historial_tareas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HistorialTareaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
