from rest_framework import generics
from rest_framework import permissions
from .serializers import TodoSerializer , TodoCompleteSerializer
from todo.models import Todo
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login , authenticate
from rest_framework.authtoken.models import Token

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user = user)
            return JsonResponse({'token':str(token)},status = 201)
        except IntegrityError:
            return JsonResponse({'error':'That username has already been taken. Please choose a new username'}, status = 400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            token, created = Token.objects.get_or_create(user = user)
            return JsonResponse({'token':str(token)},status = 200)
        return JsonResponse({'error':'Please check your credentials'}, status = 400) 
        


class ToDoCompletedList(generics.ListAPIView):
    """"""
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """"""
        user = self.request.user
        todo = Todo.objects.filter(user = user , datecompleted__isnull = False).order_by('-datecompleted')
        return todo

    
class ToDoCurrentListCreate(generics.ListCreateAPIView):
    """"""
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """listing current todo items"""
        user = self.request.user
        todo = Todo.objects.filter(user = user , datecompleted__isnull = True).order_by('-created')
        return todo

    def perform_create(self, serializer):
        """creating todo item."""
        serializer.save(user = self.request.user)


class ToDoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """"""
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """listing all todo items"""
        user = self.request.user
        todo = Todo.objects.filter(user = user )
        return todo


class ToDoComplete(generics.UpdateAPIView):
    """"""
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """listing all todo items"""
        user = self.request.user
        todo = Todo.objects.filter(user = user )
        return todo
    
    def perform_update(self, serializer):
        """Completing todo (datecompleted)"""
        serializer.instance.datecompleted = timezone.now()
        serializer.save()


    

