from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from users.models import Profile
from .models import Plant, Photo
from .permissions import CustomOnly
from .serializers import PlantSerializer,PlantCreateSerializer, PhotoSerializer,PhotoCreateSerializer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    permission_classes = [CustomOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return PlantSerializer
        return PlantCreateSerializer
    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    permission_classes = [CustomOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author','plant_id']
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return PhotoSerializer
        return PhotoCreateSerializer
    def perform_create(self,serializer):
        serializer.save(author=self.request.user)
# Create your views here.
