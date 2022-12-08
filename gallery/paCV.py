import numpy as np
import cv2
import sys
from  PIL  import Image
from urllib.request import urlopen
from datetime import datetime, timedelta
#1. 가능한 수직으로 화분과 파가 서있어야하며 파의 최고 높이가 수평일수록 좋음
#2. 파가 서로 겹치지 않을수록 좋음
#3. ratio는 가급적 작을 수록 좋음(아래로부터 30%정도가 적당너무 클시 수확을 하지 않아도 되는 시기에 수확을 해야할 수도 있음)
#4. 사진은 항상 세로로 (높이가 길게) 찍는다
import base64
import os
from .models import Photo,Plant 
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import math

def convert2NdArray(path):  #change type to ndarray and dtype is np.uint8  !!!타입을 알아야함

    img = Image.open(path)

    return np.array(img)

#상태 : 업그레이드 중 두께 가중치 추가?
#기능 : 파 넓이 계산
#입력 : image=ndarray , pakind=종류(대파=0,쪽파=1,양파=2) ,ratio=0~1, potTopCentimeter=cm
#출력 : [넓이(cm^2), 높이(cm), 무게(g)]

def paImg2AHW(img,paType, ratio,topCentimeter):#파사진을 찍었을 때 맨위 위치의 위로 파란색부분을 찾아 넓이계산
    wantToReturnOutputImg = True
    #테스트용 데이터

    # area2weight = [0.035385/2,0.016667/2,0.013846/2]#대파, 쪽파, 양파
    area2weight = [0.35385,0.16667,0.13846]#대파, 쪽파, 양파
    pxH = len(img)
    pxW = len(img[0])
    potTopPixel =int(pxH*ratio)
    #RGB로 특정색을 추출하면 어두운 사진에서 정확도가 떨어짐
    #HSV로 진행. H가 색깔, S가 채도(높으면 선명해짐), V가 명도(낮으면 어두어짐)
    
    #if you want to see output..1
    if wantToReturnOutputImg:
        original = img 
    
    newImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #S too high case
    lower_green = (25, 200, 5)
    upper_green = (97, 255, 100)
    green_mask = cv2.inRange(newImg, lower_green, upper_green)
    #S high case
    lower_green = (20, 80, 24)
    upper_green = (90, 255, 255)
    green_mask2 = cv2.inRange(newImg, lower_green, upper_green)
    #S mid case
    lower_green = (30, 40, 20)
    upper_green = (90, 80, 255)  #90 이상 재정의 
    green_mask3 = cv2.inRange(newImg, lower_green, upper_green)
    #S mid and H high case
    lower_green = (90, 45, 130)
    upper_green = (95, 70, 255)  
    green_mask4 = cv2.inRange(newImg, lower_green, upper_green)
    #S low case
    lower_green = (45, 20, 50) # 20이였는데 일단 50
    upper_green = (89, 50, 255)
    green_mask5 = cv2.inRange(newImg, lower_green, upper_green)
    
    #여러케이스를 합함
    green_mask=green_mask+green_mask2+green_mask3+green_mask4+green_mask5

    #top 아래는 모두 0으로 바꿈
    green_mask[pxH-potTopPixel:, :]=0
    
    #if you want to see output..2
    if wantToReturnOutputImg:
        newImg = cv2.bitwise_and(original, original, mask = green_mask)
        newImg = newImg[...,::-1]   
        im = Image.fromarray(newImg)
        output_path = "mask/"+datetime.now().strftime('%Y-%m-%d%H%M%S')+".jpeg"
        if os.path.exists(output_path):  #동일한 파일명이 존재할 때
            output_path = "mask/"+datetime.now().strftime('%Y-%m-%d%H%M%S')+"(1).jpeg"
        im.save(output_path)
    
    #calculate area ,height, weight
    countGreenPixel=0
    heightRow = 0
    for row in range(pxH):
        temp  =np.count_nonzero(green_mask[row])
        if heightRow==0 and temp >=3: #1 could be not accurate
            heightRow = row
        countGreenPixel+=temp
    countAllPixel = pxH*pxW
    heightCM = topCentimeter/ratio
    widthCM= heightCM*pxW/pxH
    allArea = heightCM*widthCM
    greenArea = round(allArea*countGreenPixel/countAllPixel,1)
    
    heightRows = pxH - heightRow-int(ratio*pxH)
    height = round(heightCM*heightRows/pxH,1)
    
    weight = round(greenArea*area2weight[paType],1)
    
    
    
    #if you want to see output..3
    # if wantToReturnOutputImg:
    #     return [greenArea,height,weight,newImg]

    return [greenArea,height,weight]
    
#상태 : 구현완료
#기능 : 두 이미지 파 넓이 차이 계산
#입력 : before_image=ndarray , after_image=ndarray , ratio=0~1, potTopCentimeter=cm
#출력 : 두 이미지 [넓이(cm^2), 높이(cm), 무게(g)] 의 차
def paHarvest(before_img,after_img,paType,ratio, potTopCentimeter):#수확시, 두 파사진이 동시에 왔을 때 차를 반환 완료
    diff= [round(a - b,1) for a, b in zip(paImg2AHW(before_img,paType, ratio, potTopCentimeter), paImg2AHW(after_img,paType,ratio, potTopCentimeter) )]
    if diff[0]<0 :
        return 'ERROR, pa is grown..'
    else :
        return diff
    
#상태 : 구현전
#기능 : 성장 곡선 예측, 수확시기 예측
#입력 : heightList = [[datetime1,height1],[datetime2,height2],[datetime3,height3]...]
#출력 : 수확 시기...?
#식물 번호 받아서 바로 값 수정하도록 변경함

def harvPredict(weightList,paType,id):
    #최고 높이를 찾음 거기서 harvestCriteria=2? 가 작은 날을 반환.
    #만약 최고 높이와 현재 식물의 높이가 2가 차이가 안난다고 판단되면 수확을 진행 
    #criteria of harvest

    harvestCriteria = 0.1
    
    firstDay = weightList[0][0]
    for w in weightList:
        w[0] = (w[0]-firstDay).days

    if len(weightList)<3:
        if (paType==0):appropriateWeight = 25 #대파
        elif (paType==1) : appropriateWeight=10 #쪽파
        else : appropriateWeight=10 #양파파
        return [firstDay+timedelta(days=14),round(appropriateWeight,1)]

    inputX = [ w[0] for w in weightList] #datetime
    inputY =[ w[1] for w in weightList] #weight
    for zero in range(len(inputX)):
        if inputX[zero]==0:
            inputX[zero]+=0.001
    for zero in range(len(inputY)):
        if inputY[zero]==0:
            inputY[zero]+=0.001
    
    #convert inputX shape for regression
    X = np.array([[dates] for dates in inputX])
    
    previousError = 1000000000 #previous error value
    appropriateWeight = 0 #appropriate Weight
    
    curMaxWeight = max(inputY)+0.1
    while(curMaxWeight<=70):
        tempError = 0
        #log(-y/y-1) = x 임을 이용!!!(0<y<1 이어야함)  이렇게 하면 y= 1/(1+e^-(ax+b)) 를 예측 가능!  
        #convert Y
        reductY = np.divide(np.array(inputY),curMaxWeight) #Later, we have to convert this. e^(logTheY) = input Y no is not......
        #log(-y/(y-1)) = x
        Y = np.log(np.negative(reductY)/(reductY-1))
        model = LinearRegression()
        model.fit(X,Y)
        for i in range(len(inputX)):
            ex = math.exp(model.coef_*inputX[i]+model.intercept_)
            tempError+= abs(ex*curMaxWeight/(1+ex)-inputY[i]) #평균절대오차
        # print(curMaxWeight,tempError)
        if tempError<previousError:
            previousError=tempError
            appropriateWeight=curMaxWeight
        # plt.scatter(curMaxWeight,previousError,  alpha=0.3)
        else :
            break
        curMaxWeight+=0.1
    # plt.show()
    # print("Maximum weight of this plant will be",appropriateWeight)
    
    reductY = np.divide(np.array(inputY),appropriateWeight)
    Y = np.log(np.negative(reductY)/(reductY-1))
    model = LinearRegression()
    model.fit(X,Y)

    
    if (appropriateWeight-harvestCriteria) < max(inputY):
        harvest_date = firstDay + timedelta(days=max(inputX))
    else:
        tempY = (appropriateWeight-harvestCriteria)/appropriateWeight
        tempX = (math.log(-tempY/(tempY-1))-model.intercept_)//model.coef_
        # print(tempX[0])
        # print(inputX,inputY)
        harvest_date =  firstDay + timedelta(days=int(tempX[0])+1)
        
        
    #default
    if ((harvest_date-firstDay).days<3):
        harvest_date = firstDay+timedelta(days=14)
        if (paType==0):appropriateWeight = 25 #대파
        elif (paType==1) : appropriateWeight=10 #쪽파
        else : appropriateWeight=10 #양파파
    
    #if you want to see graph
    xs = np.arange(0,50,1)
    ex =np.exp(model.coef_*xs+model.intercept_)
    ys = ex*appropriateWeight/(1+ex)
    plt.scatter(inputX,inputY,  alpha=0.3)
    plt.scatter(tempX,appropriateWeight,color='green')
    plt.plot(xs,ys,'r-',lw=3)
    plt.savefig('graph/graph'+str(id)+'.png', dpi=300)
    plt.clf()

    return [harvest_date,round(appropriateWeight,1)]
