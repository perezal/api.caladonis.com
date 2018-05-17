from rest_framework import generics, serializers
from accounts.serializers import UserSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

@permission_classes((AllowAny, ))
class AccountView(generics.CreateAPIView):

    serializer_class = UserSerializer
