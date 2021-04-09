from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.menu import views

router = DefaultRouter()
router.register('menu', views.MenuViewSet)

app_name = 'menu'

urlpatterns = [
    path('', include(router.urls))
]
