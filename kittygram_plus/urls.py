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

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url


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

schema_view = get_schema_view(
   openapi.Info(
      title="Cats API",
      default_version='v1',
      description="Документация для приложения cats проекта Kittygram",
      # terms_of_service="URL страницы с пользовательским соглашением",
      contact=openapi.Contact(email="admin@kittygram.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', 
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc'),
]


SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
} 

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