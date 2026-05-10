from django.urls import path
from . import views

app_name = 'historia'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/galeria/', views.galeria_api, name='galeria_api'),
]
