from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *


router=DefaultRouter()

router.register(r'posts',PostViewSet,basename='posts'),
router.register(r'apply', ApplyViewSet, basename='apply')


urlpatterns = [
   
    path('',include(router.urls)),
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),
   

]