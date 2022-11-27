from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,status
from users.models import Profile
from .models import Plant, Photo, Price
from .permissions import CustomOnly,IsOwner
from backend.settings import BASE_DIR,BASE_URL
from .serializers import PlantSerializer,PlantCreateSerializer, PhotoSerializer,PhotoCreateSerializer,\
    RecentPlantSerializer, GraphSerializer, HomePage_PlantSerializer,\
        PhotoTimelineSerializer,PriceSerializer,HPhotoCreateSerializer,\
            SimplePhotoSerializer, PlantPage_PlantSerializer
from urllib import parse

from .paCV import paImg2AHW,convert2NdArray
from rest_framework.views    import APIView
from rest_framework.authtoken.models  import Token

from rest_framework.decorators import api_view,permission_classes
from users.serializers import ProfileSerializer,RankProfileSerializer
import os
from rest_framework.response import Response
from datetime import datetime,timedelta



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
        print(self.request.data)
        
        
        # plant=Plant.objects.get(id=self.request.data.get('plant'))
        # img = convert2NdArray(self.request.FILES['image'])
        # msize,mheight,mweight = paImg2AHW(img,plant.plant_species,plant.pot_ratio,plant.pot_size)

        # 수확 예정 정보 계산 필요 
        # plant 값 update;
        # 수확 했을 경우에는 
        # user.profile 값 변경
        change = 0
        # 사이즈 추가 필요

        # serializer.save(author=self.request.user,size=msize,length=mheight,weight=mweight)
        plant=Plant.objects.get(id=self.request.data.get('plant'))
        photo = serializer.save(author=self.request.user)
        img0 = convert2NdArray(parse.unquote(serializer.data.get("image").replace(BASE_URL,"")))
        photo.size,photo.length,photo.weight = paImg2AHW(img0,plant.plant_species,plant.pot_ratio,plant.pot_size)
        print(photo.size,photo.length,photo.weight )
        photo.save()
# Create your views here.
import requests
import json

def rank_update():
    profiles = Profile.objects.all()
    for profile in profiles:
        profile.total_gain=int(profile.depa_weight*Price.objects.get(species=0).price\
            +profile.jjokpa_weight*Price.objects.get(species=1).price\
                +profile.onion_weight*Price.objects.get(species=2).price)

    profiles = sorted(profiles, key= lambda x: x.total_gain,reverse=True)
    for i,profile in enumerate(profiles,start=1):
        profile.rank = i

    Profile.objects.bulk_update(profiles,["total_gain","rank"])

def set_price():
    pricelist=[0,0]
    datelist=[0,0]
    delay_day=[0,1,7,14,30]
    n = 0
    resp =""
    json_data = ""
    while True:
        URL = 'https://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList&p_product_cls_code=02&p_country_code=1101&p_regday='\
            +(datetime.today()-timedelta(n)).strftime("%Y-%m-%d")+'&p_convert_kg_yn=Y&p_item_category_code=200&p_cert_key=50bda903-19bc-4821-8cae-de61be81bc71&p_cert_id=2923&p_returntype=json'
        resp =  requests.get(URL)
        json_data = json.loads(resp.text)
        if type(json_data["data"])==dict or n>5 :
            break
        n += 1

    for vege in json_data["data"]["item"]:
        if vege["item_code"]=="246" and vege["rank"]=="상품":
                if vege["kind_name"]=="대파(1kg)":
                    r_d=1
                    while vege["dpr"+str(r_d)] == '-':
                        r_d+=1
                        if r_d>5: 
                            break
                    pricelist[0]=vege["dpr"+str(r_d)]
                    datelist[0]=delay_day[r_d-1]
                if vege["kind_name"]=="쪽파(1kg)":
                    r_d=1
                    while vege["dpr"+str(r_d)] == '-':
                        r_d+=1
                        if r_d>5: 
                            break
                    pricelist[1]=vege["dpr"+str(r_d)]
                    datelist[1]=delay_day[r_d-1]
    
    if Price.objects.get(species=0).date<(datetime.today().date()-timedelta(n+datelist[0])):
        price_data0 = Price(species=0,price=int(pricelist[0].replace(",","")),date=(datetime.today().date()-timedelta(n+datelist[0]))) 
        price_data0.save()
    if Price.objects.get(species=1).date<(datetime.today().date()-timedelta(n+datelist[1])):
        price_data1 = Price(species=1,price=int(pricelist[1].replace(",","")),date=(datetime.today().date()-timedelta(n+datelist[1]))) 
        price_data1.save()


    #시세에 따른 재계산=>정렬&update
    rank_update()




@api_view(['GET'])
def homepage(request):
    profile = Profile.objects.get(user=request.user)
    serializer_profile = ProfileSerializer(profile)
    sql= \
        'select * \
            from (\
            select *,row_number() over ( partition by plant_id order by date desc) as rn\
            from gallery_photo\
        ) as t\
        where t.rn =1 and t.author_id='+str(request.user.pk)+' order by date desc;'
    images = Photo.objects.raw(sql)[:5]
    serializer_image = RecentPlantSerializer(images,many=True,context={'request':request})
    #대파가격/쪽파가격
    # price_data0 = Price(species=0,price=1,date=datetime.today().date()) 
    # price_data0.save()
    # set_price()
    return Response({'nickname':profile.nickname,'patech_indicator':cvtmoney(profile.total_gain),'img_list':serializer_image.data})

def cvtmoney(money):
    item_list=['-','교통비🚃','붕어빵⛄️','아메리카노 1잔☕️','참치김밥🐟',\
    '햄버거 세트🍔','떡볶이 1인분🍽','영화 티켓🎟','치킨 1마리🍗','한우 1인분🥩',\
        '제주도행 비행기표✈️','에어팟 맥스🎧','맥북 프로💻']
    
    price_list=[0,1200,3000,4000,5000,7000,10000,14000,20000,30000,70000,690000,2500000]
    for i,price in enumerate(price_list,start=-1):
        if money<price:
            return item_list[i]
    return item_list[-1]

@api_view(['GET'])
def plantlist(request):
    sql= \
        'select * \
            from (\
            select *,row_number() over ( partition by plant_id order by date desc) as rn\
            from gallery_photo\
        ) as t\
        where t.rn =1 and t.author_id='+str(request.user.pk)+' order by date desc;'
    images = Photo.objects.raw(sql)
    serializer_image =RecentPlantSerializer(images,many=True,context={'request':request})
    return Response({"plantlist":serializer_image.data})




@api_view(['GET'])
def plantnamecheck(request):
    true_check = Plant.objects.filter(author=request.user,plant_name=request.GET["plant_name"])
    if true_check.exists():
        return Response(status=status.HTTP_226_IM_USED)
    else:
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def nicknamecheck(request):
    true_check = Profile.objects.filter(nickname=request.GET["nickname"])
    if true_check.exists():
        return Response(status=status.HTTP_226_IM_USED)
    else:
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getphotos(request,plant_id):
    photos = Photo.objects.filter(plant=plant_id,image__isnull=False).order_by("-date")[:5]
    serializer_image = SimplePhotoSerializer(photos,many=True,context={'request':request})
    return Response({"photolist":serializer_image.data})



@api_view(['POST'])
def harvest(request):
    plant=Plant.objects.get(id=request.data.get('plant'))

    
    serializer0=HPhotoCreateSerializer(data = request.data,context={'request':request})
    weight_before=0
    weight_after=0
    if serializer0.is_valid():
        photo=serializer0.save(author=request.user,plant =plant,event_harvest=1)
        #이전사진 무게
        img0 = convert2NdArray(parse.unquote(serializer0.data.get("beforeimage").replace(BASE_URL,"")))
        photo.size,photo.length,photo.weight = paImg2AHW(img0,plant.plant_species,plant.pot_ratio,plant.pot_size)        
        photo.save()
        weight_before=photo.weight

        
        img1 = convert2NdArray(parse.unquote(serializer0.data.get("afterimage").replace(BASE_URL,"")))
        size,length,weight = paImg2AHW(img1,plant.plant_species,plant.pot_ratio,plant.pot_size)
        photo_dummy=Photo(author=request.user,plant=plant,size=size,length=length,weight=weight)
        photo_dummy.save()  
        weight_after=weight

    else:
        Response(status=status.HTTP_204_NO_CONTENT)

    # serializer1=APhotoCreateSerializer(data = request.data,context={'request':request})
    # if serializer1.is_valid():
    #     photo=serializer1.save(author=request.user,plant =plant)
    #     img1 = convert2NdArray(parse.unquote(serializer1.data.get("afterimage").replace(BASE_URL,"")))
    #     photo.size,photo.length,photo.weight = paImg2AHW(img1,plant.plant_species,plant.pot_ratio,plant.pot_size)
    #     weight_after=photo.weight
    #     photo.save()
    # else:
    #     Response(status=status.HTTP_204_NO_CONTENT)


    diff = weight_before-weight_after
    profile= Profile.objects.get(user=request.user)
    if(plant.plant_species==0):
        profile.depa_weight+=(diff)
    elif(plant.plant_species==1):
        profile.jjokpa_weight+=(diff)
    elif(plant.plant_species==2):
        profile.onion_weight+=(diff)
    profile.save()
    rank_update()
    return Response({"size_dif":weight_before-weight_after,"money":int((weight_before-weight_after)*(Price.objects.get(species=plant.plant_species).price))},status=status.HTTP_200_OK)
    
   

class PlantPageAPIVIEW(APIView):
    permission_classes = [IsOwner]
    def get(self,request,plant_id):        
        plant = Plant.objects.get(pk=plant_id)
        self.check_object_permissions(self.request, plant)
        print(plant)
        photos = Photo.objects.filter(plant=plant_id)
        serializer_plant = PlantPage_PlantSerializer(plant)
        serializer_graph = GraphSerializer(photos,many=True)
        serializer_timeline= PhotoTimelineSerializer(photos.filter(image__isnull=False),many=True,context={'request':request})
        return Response({'plant':serializer_plant.data,'graph_list':serializer_graph.data,'time_line':serializer_timeline.data})

class PatechRank(APIView):
    def get(self,request):
        #최대개수 20개 제한
        profile_list = Profile.objects.all().order_by('-total_gain')[:20]
        serializer_profiles=RankProfileSerializer(profile_list,many=True)
        user_profile = Profile.objects.get(user=request.user)
        serializer_user_profiles =RankProfileSerializer(user_profile)
        serializer_price = PriceSerializer(Price.objects.all(), many=True)
        return Response({'patech_indicator':cvtmoney(user_profile.total_gain),'user':serializer_user_profiles.data,'price':serializer_price.data,'list':serializer_profiles.data})



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
