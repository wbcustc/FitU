from rest_framework import viewsets
from serializers import UserviewSerializer
from fitu_backend.models import CustomUser
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserviewSerializer
