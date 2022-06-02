"""
Возможные реализации API
Возможные дженерики:
ListAPIView - Только Get-запросы. Возвращает один объект.
CreateAPIView - Только Post-запросы. Создает новый объект.
UpdateAPIView - Только Put и Patch-запросы. Изменяет объект.
DestroyAPIView - Только Delete-запросы. Удаляет объект.
ReadOnlyModelViewSet - вьюсет получение списка или одного объекта.
"""
from rest_framework import viewsets
from rest_framework import permissions
# from rest_framework import status # библиотека со статусами
# from rest_framework import mixins
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.views import APIView
# from django.shortcuts import get_object_or_404
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


from .models import Cat, Achievement, User # Owner
from .serializers import CatSerializer, AchievementSerializer, UserSerializer #OwnerSerializer, CatListSerializer
from .permissions import OwnerOrReadOnly, ReadOnly
from rest_framework.throttling import AnonRateThrottle
from .throttling import WorkingHoursRateThrottle
from rest_framework.pagination import LimitOffsetPagination
from .pagination import CatsPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

'''
class UpdateDeleteViewSet(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    """Вьюсет для примера. Может только обновить модель или удалить."""
    pass

class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    """Вьюсет получает объект и возвращает в get-запросе"""
    pass 


class LiqhtCatViewSet(CreateRetrieveViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
'''


class CatViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Сats."""
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    #throttle_classes = (AnonRateThrottle, WorkingHoursRateThrottle)
    #throttle_scope = 'low_request'
    # pagination_class = LimitOffsetPagination
    pagination_class = CatsPagination
    pagination_class = None
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name', 'achievements__name', 'owner__username')
    ordering_fields = ('name',)
    ordering = ('birth_year',)

    def perform_create(self, serializer):
        """Хук, который позволяет переписать
        поведение при сохранении записи
        """
        serializer.save(owner=self.request.user)
    
    def perform_update(self, serializer):
        """Хук, который позволяет переписать
        поведение при обновлении записи
        """
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


'''
    @action(detail=False, url_path='recent-white-cats')
    def recent_white_cats(self, request):
        """Нестандартное поведение вьюсета.
        Возвращает 5 последних добавленых белых котов.
        """
        cats = Cat.objects.filter(color='White')[:5]
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        """Функция определяет в каком 
        сериализаторе будет обрабатываться объект.
        Чтобы переопределить нужно убрать явное обозначение
        сериализатора и добавить эту функцию."""
        if self.action == 'list':
            return CatListSerializer
        return CatSerializer
'''




class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет пользователя.
    Унаследован от ReadOnlyModelViewSet.
    Чтобы пользователи не могли изменять данные друг друга
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

'''
class OwnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
'''

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

'''
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
    serializer = CatSerializer(cats, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def hello(request):
    """View-функция без работы с моделью. Возвращает запрос"""
    if request.method == 'POST':
        return Response({'message': 'Получены данные', 'data': request.data})
    return Response({'message': 'Это был GET-запрос!'})

'''