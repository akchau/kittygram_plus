"""
Доступные адреса
{
    "cats": "http://127.0.0.1:8000/cats/",
    "owners": "http://127.0.0.1:8000/owners/"
}

В комменариях адреса на другие реализации API

"""
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from cats.views import CatViewSet, OwnerViewSet, cat_list, APICat, APICatDetail, GenericAPICat, GenericAPICatDetail


router = DefaultRouter()
router.register('cats', CatViewSet)
router.register('owners', OwnerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

"""
   path('cats/', ..., name='api-root'), - есть только у Default. Показывает все эндпоинты.
   path('cats/', ..., name='cat-list'),
   path('cats/<int:pk>/', ..., name='cat-detail')
   через basename в роутере можно переопределить префикс
   path('cats/<int:pk>/', GenericAPICatDetail.as_view()),
   path('cats/<int:pk>/', APICatDetail.as_view()),
   path('cats/', GenericAPICat.as_view()),
   path('cats/', APICat.as_view()),
   path('cats/', cat_list),
"""