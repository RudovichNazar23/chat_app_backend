from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import User, UserSerializer
from .permissions import IsProfileOwner

from django.core.exceptions import ObjectDoesNotExist


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

    @action(detail=False, url_name="request_user", methods=["GET",], )
    def request_user(self, request):
        try:
            request_user = User.objects.get(pk=self.request.user.id)
            serialized_data = self.get_serializer_class()(request_user).data
            return Response({"data": serialized_data})
        except ObjectDoesNotExist as error:
            return Response({"data": "User does not exist"})


