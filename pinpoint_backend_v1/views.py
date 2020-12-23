from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from pinpoint_backend_v1.serializers import UserSerializer, GroupSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from pinpoint_backend_v1.models import Pin
from django.middleware import csrf
import json

@api_view(['POST'])
def login_handler(request):
  if request.method == "POST":
        # username = request.POST["username"]
        # password = request.POST["password"]
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            content = {'Status': 'Login successful!'}
            return Response(content, status=status.HTTP_200_OK)
        content = {'Status': 'Login unsuccessful!'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)      

@api_view(['GET'])
def get_session_token(request):
  return Response({'SessionToken': csrf.get_token(request)})

@api_view(['POST'])
@authentication_classes([])
def signup_handler(request):
  if request.method == "POST":
    if User.objects.filter(username=request.data['username']).exists():
      content = {'Status': 'Username already exists!'}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif User.objects.filter(email=request.data['email']).exists():
      content = {'Status': 'Email already exists!'}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
      user = User.objects.create_user(username=request.data['username'], email=request.data['email'], password=request.data['password'])
      content = {'Status': 'User profile successfully created!'}
      return Response(content, status=status.HTTP_200_OK)
  
  content = {'Status': 'User was not created!'}
  return Response(content, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_pin_handler(request):
  if request.method == "POST":
    if not Pin.objects.filter(address=request.data['address'], user_id=request.user.id).exists():
      address = request.data["address"]
      new_pin = Pin(address=address, user_id=request.user.id, username=request.user.username)
      new_pin.save()
      content = {'Status': 'Pin successfully created!'}
      return Response(content, status=status.HTTP_200_OK)
    else:
      content = {'Status': 'Pin already exists!'}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)
  else:
    content = {'Status': 'Unable to create pin!'}
    return Response(content, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_pins_handler(request):
  if request.method == "GET":
    addresses = list(Pin.objects.filter(user_id=request.user.id).values())
    content = {'Pins': addresses}
    return Response(content, status=status.HTTP_200_OK)
  else:
    content = {'Status': 'Unable to retrieve pins!'}
    return Response(content, status=status.HTTP_400_BAD_REQUEST)


'''
@api_view(['GET'])
@authentication_classes([])
def logout_handler(request):
  logout(request)
  content = {'Status': 'User successfully logged out!'}
  return Response(content, status=status.HTTP_200_OK)
'''