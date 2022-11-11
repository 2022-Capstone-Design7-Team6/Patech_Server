from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from users.models import Profile
from .models import Plant, Photo
from .permissions import CustomOnly,IsOwner
from .serializers import PlantSerializer,PlantCreateSerializer, PhotoSerializer,PhotoCreateSerializer,\
    RecentPlantSerializer, GraphSerializer, HomePage_PlantSerializer,\
        PhotoTimelineSerializer

from .paCV import paPic,convert2NdArray
from rest_framework.views    import APIView
from rest_framework.authtoken.models  import Token

from rest_framework.decorators import api_view,permission_classes
from users.serializers import ProfileSerializer

from rest_framework.response import Response
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
    filterset_fields = ['author','plant']
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return PhotoSerializer
        return PhotoCreateSerializer
    def perform_create(self,serializer):
        # 데이터 저장 전에 size 계산 한 뒤 투입
        plant=Plant.objects.get(id=self.request.data.get('plant'))
        img = convert2NdArray(self.request.FILES['image'])
        msize = paPic(img,plant.pot_ratio,plant.pot_size)
        # 수확 예정 정보 계산 필요 
        # plant 값 update;
        # 수확 했을 경우에는 
        # user.profile 값 변경
        change = 0
        # 사이즈 추가 필요
        serializer.save(author=self.request.user,size=msize)
# Create your views here.

@api_view(['GET'])
def homepage(request):
    serializer_profile = ProfileSerializer(Profile.objects.get(user=request.user))
    sql='select gallery_photo.* from gallery_photo inner join (select max(date) as date,author_id from gallery_photo where author_id = '+str(request.user.pk)+' group by plant_id ) as b on gallery_photo.date = b.date order by date desc limit 5'
    images = Photo.objects.raw(sql)
    serializer_image = RecentPlantSerializer(images,many=True,context={'request':request})
    return Response({'nickname':serializer_profile.data,'img_list':serializer_image.data})

@api_view(['GET'])
def plantlist(request):
    sql='select gallery_photo.* from gallery_photo inner join (select max(date) as date,author_id from gallery_photo where author_id = '+str(request.user.pk)+' group by plant_id ) as b on gallery_photo.date = b.date order by date desc'
    images = Photo.objects.raw(sql)
    serializer_image = RecentPlantSerializer(images,many=True,context={'request':request})
    return Response(serializer_image.data)



class PlantPageAPIVIEW(APIView):
    permission_classes = [IsOwner]
    def get(self,request):
        plant_id = request.data.get("plant")
        plant = Plant.objects.get(pk=plant_id)
        self.check_object_permissions(self.request, plant)
        print(plant)
        photos = Photo.objects.filter(plant=plant_id)
        serializer_plant = HomePage_PlantSerializer(plant)
        serializer_graph = GraphSerializer(photos,many=True)
        serializer_timeline= PhotoTimelineSerializer(photos,many=True,context={'request':request})
        return Response({'plant':serializer_plant.data,'graph_list':serializer_graph.data,'time_line':serializer_timeline.data})


# 가장 최근 식물 2개
# 최근 시세 (시세 가져온 일자, 가격)
# user nickname
# 파테크 지표 (ex) “치킨 한 마리”

# 파 리스트 - (최대5개) 사용자가 최근에 일지를 등록한 순
# 카테고리(대파, 양파, 쪽파)
# 파 이름
# 식물 이미지 (가장 최근에 촬영한 사진)
# D+80 정보(int)
# 수확예정 정보
