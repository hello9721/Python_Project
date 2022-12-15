from django.shortcuts import render
from .models import *
from .API_TO_DB import *
from .LOC_TO_XY import *

def home(request):                          # 홈페이지 구성

    c1 = Location.objects.values('one')     # one 열 정보가 들어갈 변수
    c2 = []                                 # one에 따른 two 열 정보가 들어갈 변수
    c3 = []                                 # one과 two에 따른 thr 열 정보가 들어갈 변수

    Rc1 = []                                # 실제 select에 들어갈 리스트                                
    Rc2 = []
    Rc3 = []
                                            # 앞 변수가 선택되기 전에는 뒷 변수는 비어있음.
    
    cst = ['vFcst', 'sFcst', 'sNcst']       # 날씨 정보 조회 시 단기예보, 초단기예보, 초단기실황 을 각각 조회 하게 해줄 설정값

    if request.GET == {}:                   # 최초 접속시 get 으로 들어오는 값이 없을 때

        address = ''                        # address 변수 미리 선언
        ip = get_ip(request)                # LOC_TO_XY 의 get_ip 를 통해 IP 주소 가져오기

        for i in cst:                       # IP 주소에 따라 x, y 값과 주소를 가져오고 x, y 값으로 api에 접속, 날씨 정보를 DB에 저장 
        
            temp, address = get_data(i, ip)
            data_to_DB(temp, i)

        val = [address[0], address[1], address[2]]
                                            # select의 selected 되는 값을 주소 값으로 설정
                                             
    elif request.GET != {}:                 # 사용자의 설정된 값이 있어서 get 으로 들어오는 값이 있을 때
        
        prev = request.GET.get('prev').split('/')
                                            # 이전 설정 값이 저장된 값에서
        val = [prev[0], prev[1], prev[2]]   # val 값을 설정

        if request.GET.get('one') != val[0]:
                                            # one의 값이 이전 설정 값과 다르다면 실행

            get_one = request.GET.get('one')
            val[0] = get_one                # val[0] 은 one에서 가져온 값으로
            val[1] = '=== 구 ==='           # 나머지는 초기화
            val[2] = '=== 동 ==='

            c2 = Location.objects.filter(one__contains=get_one).values('two')
                                            # c2에 one 값을 가진 two열의 값 저장

        elif request.GET.get('two') != val[1]:
                                            # one이 이전 값과 같을 때 two의 값이 이전 설정 값과 다르다면 실행

            get_two = request.GET.get('two')
            val[1] = get_two                # val[0]은 이전 값 그대로, val[1]은 two의 값 저장
            val[2] = '=== 동 ==='           # val[2] 초기화

            c3 = Location.objects.filter(one__contains=val[0]).filter(two__contains=get_two).values('thr')
            c2 = Location.objects.filter(one__contains=val[0]).values('two')
                                            # c3에 one 값과 two 값을 가진 thr열의 값저장
                                            # c2에 이전 값과 같은 값이 유지되도록 설정

        elif request.GET.get('thr') != val[2]:
                                            # one, two가 이전 값과 같을 때 thr의 값이 이전 설정 값과 다르다면 실행

            get_thr = request.GET.get('thr')
            val[2] = get_thr                # val[0], val[1]는 그대로, val[2]만 이번에 가져온 thr 값으로 저장

            c3 = Location.objects.filter(one__contains=val[0]).filter(two__contains=val[1]).values('thr')
            c2 = Location.objects.filter(one__contains=val[0]).values('two')
                                            # c2, c3에 이전 값과 같은 값이 유지되도록 설정
            for i in cst:
                                            # 마지막 요소까지 모두 선택된 상태이기에 그 값으로 x, y 값을 가져와 api에 조회 및 DB에 날씨 정보 저장
                temp, useless = get_data(i, get_thr)
                data_to_DB(temp, i)

    for i in c1:                            # c1 이나 c2, c3 에 값이 들어있다면 그 값으로 select 에 들어갈 리스트 구성
        if i not in Rc1: Rc1.append(i)

    for i in c2:
        if i not in Rc2: Rc2.append(i)

    for i in c3:
        if i not in Rc3: Rc3.append(i)

    return render(request, "home/index.html", {"Rc1": Rc1, "Rc2": Rc2, "Rc3": Rc3, 'val' : val})