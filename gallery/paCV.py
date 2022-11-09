import numpy as np
import cv2
import sys
from  PIL  import Image
from urllib.request import urlopen
#1. 가능한 수직으로 화분과 파가 서있어야하며 파의 최고 높이가 수평일수록 좋음
#2. 파가 서로 겹치지 않을수록 좋음
#3. ratio는 가급적 작을 수록 좋음(아래로부터 30%정도가 적당너무 클시 수확을 하지 않아도 되는 시기에 수확을 해야할 수도 있음)
#4. 사진은 항상 세로로 (높이가 길게) 찍는다

def convert2NdArray(f):  #change type to ndarray and dtype is np.uint8  !!!타입을 알아야함

    myfile = f.read()
    imageBGR = cv2.imdecode(np.frombuffer(myfile , np.uint8), cv2.IMREAD_UNCHANGED)
    # imageRGB = cv2.cvtColor(imageBGR , cv2.COLOR_BGR2RGB)
    return imageBGR

def potTopDrawer(img):#사용자에게 직접 받는것이 빠를듯 화분 맨위의 위치와 ratio 파악  !!!여기서 하면 상당히 비효율적
    #중앙하단에 범위를 설정하여 grabcut을 진행! 
    mask = np.zeros(img.shape[:2],np.uint8)
    
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65), np.float64)
    
    rect = (1,1,665,344)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]
    
    tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
    b,g,r = cv2.split(img)
    rgba = [b,g,r,alpha]
    newImg = cv2.merge(rgba,4)
    
    cv2.imshow('wow',newImg)
    cv2.waitKey(0)
    
    top=100
    ratio = 100 #pot real height and picture heigth ratio
    return newImg, top, ratio

def picTrans(img):#사진을 반투명하게 만듬 완료
    transparency = 127 #min 0. max 255
    b, g, r = cv2.split(img)
    mask=np.full((len(img),len(img[0])),transparency,dtype=np.uint8)
    newImg = cv2.merge([b, g, r, mask], 4)
    # write as png which keeps alpha channel 
    #cv2.imwrite('result.png', newImg)
    return newImg

def paPic(img,ratio, potTopCentimeter):#파사진을 찍었을 때 맨위 위치의 위로 파란색부분을 찾아 넓이계산
    print("WTF")
    print(type(img))
    potTopPixel =int(len(img)*ratio)
    #RGB로 특정색을 추출하면 어두운 사진에서 정확도가 떨어짐
    #HSV로 진행. H가 색깔, S가 채도(높으면 선명해짐), V가 명도(낮으면 어두어짐)
    original = img #출력원할떄..
    newImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #명도 high case 
    lower_green = (35, 25, 100)
    upper_green = (85, 255, 255)
    green_mask = cv2.inRange(newImg, lower_green, upper_green)
    #채도 high case
    lower_green = (35, 100, 25)
    upper_green = (85, 255, 255)
    green_mask2 = cv2.inRange(newImg, lower_green, upper_green)
    #여러케이스를 합함
    green_mask+=green_mask2
    #top 아래는 모두 0으로 바꿈
    green_mask[len(img)-potTopPixel:, :]=0
    
    # cv2.imwrite('result5.png', green_mask)
    #if you want to see output..
    newImg = cv2.bitwise_and(original, original, mask = green_mask)
    # cv2.imwrite('result4.png', newImg)

    #calculate area
    countPixel=np.count_nonzero(green_mask)
    countAllPixel = len(img)*len(img[0])
    heightCM = potTopCentimeter/ratio
    widthCM= heightCM*len(img[0])/len(img)
    allArea = heightCM*widthCM
    print(countPixel*allArea/countAllPixel)
    return round(countPixel*allArea/countAllPixel,1)
    
def paHarv(before_img,after_img,ratio, potTopCentimeter):#수확시, 두 파사진이 동시에 왔을 때 차를 반환 완료
    areaDiff= paPic(after_img,ratio, potTopCentimeter)-paPic(before_img,ratio, potTopCentimeter) 
    if areaDiff<=0 :
        return 'ERROR, pa is grown..'
    else :
        return areaDiff
    
def drawGraph(areaList):#넓이가 저장된 list 에 대해 graph 로 반환 !!!근데 이걸 만들어서 줘도 되나..?
    #areaList contain pot's area
    newImg = areaList
    #return graph image?
    return newImg