from django.shortcuts import render
from django.http import HttpResponse
from .models import Essay
import pandas as pd


def home (ss) :
    return render(ss,"Home.html",{})


def page1 (ss) :
    return render(ss,"page1.html",{})

def mi(ss) :
    
    df = pd.read_csv("C:/Users/user07/dd.csv",encoding = "euc-kr")
    c1= df["1단계"] # 각각 지역별로 저장함
    c2= df["2단계"]
    c3= df["3단계"]

    #c1 = list(set(c1)) # 각각의 지역별로 저장한 값을 공통된 값이 안나오게 제거
    #c2 = list(set(c2))
    #c3 = list(set(c3))


    Rc1 = []
    Rc2 = []
    Rc3 = []
    for i in c1: # for문을 사용하여 공통된 값을 제거하는 방법
        if i not in Rc1:
            Rc1.append(i)

    for i in c2: # for문을 사용하여 공통된 값을 제거하는 방법
        if i not in Rc2:
            Rc2.append(i)

    for i in c3: # for문을 사용하여 공통된 값을 제거하는 방법
        if i not in Rc3:
            Rc3.append(i)






    return render(ss,"mi.html",{"Rc1": Rc1,"Rc2": Rc2,"Rc3": Rc3,})
    
# Create your views here.          
