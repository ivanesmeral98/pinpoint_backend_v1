from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from pinpoint_backend_v1.serializers import UserSerializer, GroupSerializer
from django.views.decorators.csrf import csrf_exempt
from braces.views import CsrfExemptMixin
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response

class UserViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = []
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
  #  permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    authentication_classes = []
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@authentication_classes([])
def hello_world(request):
    return Response({"message": "Hello, world!"})

