from django.urls import path, include
from .views import  CreateToDo, UpdateToDo, DetailToDo, delete_view, list_view
from . import views
from django.contrib.auth.decorators import login_required 

urlpatterns = [
    path('', list_view, name=""),
    path('list', login_required(list_view), name="to_do_list"),
    path('create/', CreateToDo.as_view(), name="to_do_create"),
    path('detail/<int:pk>', DetailToDo.as_view(), name="to_do_detail"),
    path('uptade/<int:pk>', UpdateToDo.as_view(), name="to_do_uptade"),
    path('delete/<int:pk>/', delete_view, name='to_do_delete'),
    path('accounts/', include('django.contrib.auth.urls')), 
]