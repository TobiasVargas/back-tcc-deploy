from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.api.serializers import UserProfileSerializer, UserSerializer
from core.models import UserProfile
from django.contrib.auth.models import User


class UserProfileViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_existe = User.objects.filter(username=serializer.data['username']).first()
        if user_existe:
            return Response(data={'error': 'Usuário já cadastrado!'}, status=status.HTTP_400_BAD_REQUEST)

        novo_user = User()
        novo_user.username = serializer.data['username']
        novo_user.email = serializer.data['email']
        novo_user.password = make_password(serializer.data['password'])
        novo_user.first_name = serializer.data['first_name']
        novo_user.last_name = serializer.data['last_name']
        novo_user.save()

        novo_user_profile = UserProfile()
        novo_user_profile.is_analista_de_testes = serializer.data['is_analista_de_testes']
        novo_user_profile.is_tester = serializer.data['is_tester']
        novo_user_profile.user = novo_user
        novo_user_profile.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def logado(self, request):
        if request.user.is_anonymous:
            print('1')
            return Response(data={}, status=status.HTTP_403_FORBIDDEN)
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if not user_profile:
            print('2')
            return Response(data={}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
