from django.contrib.auth.models import User
from rest_framework import generics,status
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from .permission import CustomReadOnly
from rest_framework.authtoken.models  import Token
class RegisterView(generics.CreateAPIView):
    queryset= User.objects.all()
    serializer_class= RegisterSerializer

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=False)
            user=serializer.save()
        except:
            return Response({"status":status.HTTP_403_FORBIDDEN,"pk":None,"token":None,"nickname":None})
        
        token=Token.objects.get(user=user)
        msg=status.HTTP_200_OK
        nickname=self.request.data.get("nickname")
        profile=Profile.objects.get(user=user)
        if Profile.objects.exclude(user=user).filter(nickname=nickname).exists():
            msg=status.HTTP_205_RESET_CONTENT
        else:
            profile.nickname=nickname
            profile.save()
        return Response({"status":msg,"pk":token.user_id,"token": token.key,"nickname":profile.nickname})


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({"status":status.HTTP_403_FORBIDDEN,"pk":None,"token":None})
        token = serializer.validated_data
        return Response({"status":status.HTTP_200_OK,"pk":token.user_id,"token": token.key})


from .models import Profile

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [CustomReadOnly]
    queryset = Profile.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = ProfileSerializer
    
@api_view(['PUT'])
def chgnickname(request):
    profile=Profile.objects.get(user=request.user)
    if Profile.objects.exclude(user=request.user).filter(nickname=request.data.get('nickname')).exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    profile.nickname=request.data.get('nickname')
    profile.save()
    return Response(status=status.HTTP_200_OK)

