from django.urls import path , include
from . import views

urlpatterns = [
    path('todos/',views.ToDoCurrentListCreate.as_view()),
    path('todos/<int:pk>',views.ToDoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete',views.ToDoComplete.as_view()),
    path('todos/completed',views.ToDoCompletedList.as_view()),
    #creating token
    path('signup',views.signup),
    #get token
    path('login',views.login),
]

