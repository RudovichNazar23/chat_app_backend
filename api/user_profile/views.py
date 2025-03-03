from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from .serializers import User, UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny,]

    def get_permissions(self):
        permissions_classes = []
        if self.action == "create":
            permissions_classes = [permissions.AllowAny,]
        return [permission() for permission in permissions_classes]
