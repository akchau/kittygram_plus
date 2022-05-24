"""
Доступные адреса
{
    "cats": "http://127.0.0.1:8000/cats/",
    "owners": "http://127.0.0.1:8000/owners/"
}

В комменариях адреса на другие реализации API

"""
from django.urls import include, path
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from cats import views # вью-функции приложения cats
from rest_framework.authtoken.views import obtain_auth_token # вью-функция для получения токена



router = DefaultRouter()
router.register(r'cats', views.CatViewSet)
# router.register(r'owners', views.OwnerViewSet)
router.register(r'achivement', views.AchievementViewSet)
# router.register(r'mycats', views.LiqhtCatViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token), # путь для аутентификации по AuthTokken
    path('auth/', include('djoser.urls')), # путь для аутентификации по Djoser+JWT
    path('auth/', include('djoser.urls.jwt')), # путь для аутентификации по Djoser+JWT
]

'''
   path('cats/', ..., name='api-root'), - есть только у Default. Показывает все эндпоинты.
   path('cats/', ..., name='cat-list'),
   path('cats/<int:pk>/', ..., name='cat-detail')
   через basename в роутере можно переопределить префикс
   path('cats/<int:pk>/', GenericAPICatDetail.as_view()),
   path('cats/<int:pk>/', APICatDetail.as_view()),
   path('cats/', GenericAPICat.as_view()),
   path('cats/', APICat.as_view()),
   path('cats/', cat_list),
'''