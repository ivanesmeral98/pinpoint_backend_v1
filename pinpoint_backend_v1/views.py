from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from pinpoint_backend_v1.serializers import UserSerializer, GroupSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response

'''
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = []
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    authentication_classes = []
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
'''
@api_view(['POST'])
@authentication_classes([])
def login_handler(request):
  if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            content = {'Status': 'Login successful!'}
            return Response(content, status=status.HTTP_200_OK)
        content = {'Status': 'Login unsuccessful!'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)      
  
@api_view(['POST'])
@authentication_classes([])
def signup_handler(request):
  if request.method == "POST":
    if User.objects.filter(username=request.POST['username']).exists():
      content = {'Status': 'Username already exists!'}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif User.objects.filter(email=request.POST['email']).exists():
      content = {'Status': 'Email already exists!'}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
      user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
      content = {'Status': 'User successfully created!'}
      return Response(content, status=status.HTTP_200_OK)
  
  content = {'Status': 'User was not created!'}
  return Response(content, status=status.HTTP_400_BAD_REQUEST)

'''
@api_view(['GET'])
@authentication_classes([])
def logout_handler(request):
  logout(request)
  content = {'Status': 'User successfully logged out!'}
  return Response(content, status=status.HTTP_200_OK)
'''