
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, viewsets, status
from simple import models as simple_models
from simple import serializers as simple_serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from simple import permissions as simple_permissions
from rest_framework.authentication import TokenAuthentication


class CreateUser(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user_data = request.data
        serializer = simple_serializers.UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Login(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None or password is None:
            return Response({'error':'Please provide both username and password'})
        else:
            user = simple_models.MyUser.objects.get(username=username, password=password)
            if not user:
                return Response(
                    {'error':'Invalid Credentials'},
                    status=status.HTTP_404_NOT_FOUND
                )
            token, _ = Token.objects.get_or_create(user=user)
            user.access_token = token.key
            user.save()
            return Response({
                'token':token.key},
                status=status.HTTP_200_OK
            )


class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = simple_models.MyUser.objects.all()
    serializer_class = simple_serializers.UserSerializer
    permissions = (permissions.IsAuthenticatedOrReadOnly,
                   simple_permissions.IsOwnerOrReadOnly,)
    authentication_classes = (
        TokenAuthentication,
    )

class IssuesViewSet(viewsets.ModelViewSet):

    queryset = simple_models.Issue.objects.all()
    serializer_class = simple_serializers.IssueSerializer
    permissions = (permissions.IsAuthenticated,
                   simple_permissions.IsOwnerOrReadOnly,)
    authentication_classes = (
        TokenAuthentication,
    )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


