from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from .serializers import User, UserSerializer
from .permissions import IsProfileOwner


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny,]

    def get_permissions(self):
        permissions_classes = []
        if self.action == "create":
            permissions_classes = [permissions.AllowAny,]
        elif self.action == "list":
            permissions_classes = [permissions.IsAuthenticated,]
        elif self.action in ("update", "partial_update"):
            permissions_classes = [permissions.IsAuthenticated, IsProfileOwner]
        return [permission() for permission in permissions_classes]

    def get_queryset(self):
        if self.action == "list":
            request_user_username = self.request.user.username
            queryset = User.objects.all().exclude(username=request_user_username)
            return queryset
        else:
            return super().get_queryset()
