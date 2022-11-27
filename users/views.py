from django.contrib.auth.models import User
from rest_framework import generics,status
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from .permission import CustomReadOnly
class RegisterView(generics.CreateAPIView):
    queryset= User.objects.all()
    serializer_class= RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({"pk":token.user_id,"token": token.key},status=status.HTTP_200_OK)


from .models import Profile

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [CustomReadOnly]
    queryset = Profile.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = ProfileSerializer


