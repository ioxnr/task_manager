from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.contrib import messages, auth
from rest_framework import viewsets, permissions, status
from .serializers import TaskSerializer, RegistrationSerializer


# Create your views here.

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List': '/task-list/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:primary_key>/',
        'History': '/task-history/<str:primary_key>/',
        'SortByStatus': '/sort-by-status/',
        'SortByDoneDate': '/sort-by-done-date/'
    }
    return Response(api_urls)


@api_view(['POST'])
def registration(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Successfully registered a new user."
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def task_list(request):
    user = auth.get_user(request)
    tasks = Task.objects.filter(assignee=user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def task_create(request):
    user = request.user
    task = Task(assignee=user)
    serializer = TaskSerializer(task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def task_update(request, primary_key):
    task = Task.objects.get(id=primary_key)
    user = request.user
    if task.assignee != user:
        return Response({'response': 'You don\'t have permission to edit that task'})
    serializer = TaskSerializer(instance=task, data=request.data, partial=True)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["success"] = "Update successful"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def task_history(request, primary_key):
    task_history = Task.history.filter(id=primary_key)
    serializer = TaskSerializer(task_history, many=True)
    return Response(serializer.data)


class ApiTaskView(ListAPIView):
    queryset = Task.objects.all()
    serializer = TaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('status', 'done_date')

