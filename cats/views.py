"""
Возможные реализации API
Возможные дженерики:
ListAPIView - Только Get-запросы. Возвращает один объект.
CreateAPIView - Только Post-запросы. Создает новый объект.
UpdateAPIView - Только Put и Patch-запросы. Изменяет объект.
DestroyAPIView - Только Delete-запросы. Удаляет объект.
"""
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Cat
from .serializers import CatSerializer

from .models import Cat, Owner
from .serializers import CatSerializer, OwnerSerializer


class CatViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Сats."""
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Сats."""
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class CatReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """Джерик для модели Cat. Только чтение."""
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class GenericAPICat(ListCreateAPIView):
    """Джерик для модели Cat."""
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class GenericAPICatDetail(RetrieveUpdateDestroyAPIView):
    """Джерик для конкретной модели Cat."""
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class APICat(APIView):
    """Низкоуровневый view-class для списка записей и добавления записи."""
    def get(self, request):
        cats = Cat.objects.all()
        serializer = CatSerializer(cats, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CatSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APICatDetail(APIView):
    """Низкоуровневый view-class для конкретной записи."""
    def get(self, request, pk):
        cat = get_object_or_404(Cat, pk=pk)
        serializer = CatSerializer(cat)
        return Response(serializer.data)
    def put(self, request, pk):
        cat = get_object_or_404(Cat, pk=pk)
        serializer = CatSerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        cat = get_object_or_404(Cat, pk=pk)
        serializer = CatSerializer(cat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        cat = get_object_or_404(Cat, pk=pk)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def cat_list(request):
    """view-функция для API."""
    if request.method == 'POST':
        serializer = CatSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    cats = Cat.objects.all()
    serializer = CatSerializer(cats, many=True, partial=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def hello(request):
    """View-функция без работы с моделью. Возвращает запрос"""
    if request.method == 'POST':
        return Response({'message': 'Получены данные', 'data': request.data})
    return Response({'message': 'Это был GET-запрос!'})