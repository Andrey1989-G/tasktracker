from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer

# Create your views here.


class UserCreateAPIView(generics.CreateAPIView):
    """вьюшка для создания юзера"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
