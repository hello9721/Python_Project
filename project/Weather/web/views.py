from django.shortcuts import render
from .models import *
from .API_TO_DB import *
from .LOC_TO_XY import *

def home(request):                          # 홈페이지 구성

    get_one = ""
    get_two = ""
    get_thr = ""

    c1 = Location.objects.values_list('one', flat=True)     # one 열 정보가 들어갈 변수
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

        get_one, get_two, get_thr = address[0], address[1], address[2]

        c2 = Location.objects.filter(one__contains=val[0]).values_list('two', flat=True)
        c3 = Location.objects.filter(one__contains=val[0]).filter(two__contains=val[1]).values_list('thr', flat=True)
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

            c2 = Location.objects.filter(one__contains=get_one).values_list('two', flat=True)
                                            # c2에 one 값을 가진 two열의 값 저장

        elif request.GET.get('two') != val[1]:
                                            # one이 이전 값과 같을 때 two의 값이 이전 설정 값과 다르다면 실행
            get_one = val[0]
            get_two = request.GET.get('two')
            val[1] = get_two                # val[0]은 이전 값 그대로, val[1]은 two의 값 저장
            val[2] = '=== 동 ==='           # val[2] 초기화

            c3 = Location.objects.filter(one__contains=val[0]).filter(two__contains=get_two).values_list('thr', flat=True)
            c2 = Location.objects.filter(one__contains=val[0]).values_list('two', flat=True)
                                            # c3에 one 값과 two 값을 가진 thr열의 값저장
                                            # c2에 이전 값과 같은 값이 유지되도록 설정

        elif request.GET.get('thr') != val[2]:
                                            # one, two가 이전 값과 같을 때 thr의 값이 이전 설정 값과 다르다면 실행
            get_one = val[0]
            get_two = val[1]
            get_thr = request.GET.get('thr')
            val[2] = get_thr                # val[0], val[1]는 그대로, val[2]만 이번에 가져온 thr 값으로 저장

            c3 = Location.objects.filter(one__contains=val[0]).filter(two__contains=val[1]).values_list('thr', flat=True)
            c2 = Location.objects.filter(one__contains=val[0]).values_list('two', flat=True)
                                            # c2, c3에 이전 값과 같은 값이 유지되도록 설정
            if val[2] != '=== 동 ===':
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

    if get_one in Rc1: Rc1.remove(get_one)
    if get_two in Rc2: Rc2.remove(get_two)
    if get_thr in Rc3: Rc3.remove(get_thr)

    # sFcst 

    sFcst_datetime = Srtfcst.objects.values_list('datetime', flat=True)
    sFcst_t1h = Srtfcst.objects.values_list('t1h', flat=True)
    sFcst_rn1 = Srtfcst.objects.values_list('rn1', flat=True)
    sFcst_sky = Srtfcst.objects.values_list('sky', flat=True)
    sFcst_reh = Srtfcst.objects.values_list('reh', flat=True)
    sFcst_pty = Srtfcst.objects.values_list('pty', flat=True)
    sFcst_vec = Srtfcst.objects.values_list('vec', flat=True)
    sFcst_wsd = Srtfcst.objects.values_list('wsd', flat=True)
    sFcst_uuu = Srtfcst.objects.values_list('uuu', flat=True)
    sFcst_vvv = Srtfcst.objects.values_list('vvv', flat=True)
    sFcst_lgt = Srtfcst.objects.values_list('lgt', flat=True)

    sFcst_datetime_lst = list(sFcst_datetime)
    filter_datetime = []

    for i in range(len(sFcst_datetime_lst)):
        
        sFcst_datetime_lst[i] = sFcst_datetime_lst[i].split(" ")
        filter_datetime.append((sFcst_datetime_lst[i][0], sFcst_datetime_lst[i][1]))
        sFcst_datetime_lst[i] = sFcst_datetime_lst[i][1][0:2], sFcst_datetime_lst[i][1][2:4]
    
    
    sFcst_tbl = {"datetime" : sFcst_datetime_lst, 't1h' : sFcst_t1h, 'rn1' : sFcst_rn1, 'sky' : sFcst_sky, 'reh' : sFcst_reh, 'pty' : sFcst_pty, 'vec' : sFcst_vec, 'wsd' : sFcst_wsd, 'uuu' : sFcst_uuu, 'vvv' : sFcst_vvv, 'lgt' : sFcst_lgt}

    # sNcst
    sNcst_tbl = Srtncst.objects.all()

    # 최근 6시간 강수량
    vFcst_pop = []

    for i in filter_datetime:

        temp = Vilagefcst.objects.filter(datetime__contains = str(i[0])).filter(datetime__contains = str(i[1])).values()
        vFcst_pop.append(temp[0]['pop'])

    # today min, max temperature
    date, a, b = get_now()              # 여기서 date만 사용할 것.

    temp_lst = Vilagefcst.objects.values_list("tmp", flat=True).filter(datetime__contains=date)
    temp = []
    for i in temp_lst:
        temp.append(int(i))

    today_tmx = max(temp)               # 당일 최고기온
    today_tmn = min(temp)               # 당일 최저기온


    # one days later
    # one_pop_lst : 강수 / one_reh_lst : 습도 / one_tmp_lst : 온도
    # one_tmx : 최고기온 / one_tmn : 최저기온
    date = str(int(date) + 1)           # +1 일
    one_pop = Vilagefcst.objects.values_list("pop", flat=True).filter(datetime__contains=date)
    one_reh = Vilagefcst.objects.values_list("reh", flat=True).filter(datetime__contains=date)
    one_tmp = Vilagefcst.objects.values_list("tmp", flat=True).filter(datetime__contains=date)
    one_sky = Vilagefcst.objects.values_list("sky", flat=True).filter(datetime__contains=date)

    sky_lst = ['sunny', 'sunny', 'cloudy', 'cloudy', 'cloud']
    one_sky_cnt = [0] * len(sky_lst)
    
    for i in one_sky:
        if i in sky_lst:
            idx = sky_lst.index(i)
            one_sky_cnt[idx] += 1
            
    one_sky = sky_lst[one_sky_cnt.index(max(one_sky_cnt))]
    
    one_pop_lst = []
    one_reh_lst = []
    one_tmp_lst = []

    for i in [0,8,16]:

        sum = 0
        for x in one_pop[i:i+8]:        # 강수 평균
            sum += int(x)

        one_pop_lst.append(round(sum//8))

        sum = 0
        for x in one_reh[i:i+8]:        # 습도 평균
            sum += int(x)
        one_reh_lst.append(round(sum//8))

        sum = 0
        for x in one_tmp[i:i+8]:        # 온도 평균
            sum += int(x)
        one_tmp_lst.append(round(sum//8))
    
    temp = []
    for i in one_tmp:
        temp.append(int(i))

    one_tmx = max(temp)                 # 최고기온
    one_tmn = min(temp)                 # 최저기온    


    # two days later
    date = str(int(date) + 1)           # +2 일
    two_pop = Vilagefcst.objects.values_list("pop", flat=True).filter(datetime__contains=date)
    two_reh = Vilagefcst.objects.values_list("reh", flat=True).filter(datetime__contains=date)
    two_tmp = Vilagefcst.objects.values_list("tmp", flat=True).filter(datetime__contains=date)
    two_sky = Vilagefcst.objects.values_list("sky", flat=True).filter(datetime__contains=date)

    two_sky_cnt = [0] * len(sky_lst)
    
    for i in two_sky:
        if i in sky_lst:
            idx = sky_lst.index(i)
            two_sky_cnt[idx] += 1

    two_sky = sky_lst[two_sky_cnt.index(max(two_sky_cnt))]
    
    two_pop_lst = []
    two_reh_lst = []
    two_tmp_lst = []

    for i in [0,8,16]:

        sum = 0
        for x in two_pop[i:i+8]:        # 강수 평균
            sum += int(x)

        two_pop_lst.append(round(sum//8))

        sum = 0
        for x in two_reh[i:i+8]:        # 습도 평균
            sum += int(x)
        two_reh_lst.append(round(sum//8))

        sum = 0
        for x in two_tmp[i:i+8]:        # 온도 평균
            sum += int(x)
        two_tmp_lst.append(round(sum//8))

    temp = []
    for i in two_tmp:
        temp.append(int(i))

    two_tmx = max(temp)                 # 최고기온
    two_tmn = min(temp)                 # 최저기온

    one_date, two_date = get_tomm()

    one_lst = {"one_pop_lst" : one_pop_lst, "one_reh_lst" : one_reh_lst, "one_tmp_lst" : one_tmp_lst, "one_tmx" : one_tmx, "one_tmn" : one_tmn, 'date' : one_date, 'one_sky' : one_sky}
    two_lst = {"two_pop_lst" : two_pop_lst, "two_reh_lst" : two_reh_lst, "two_tmp_lst" : two_tmp_lst, "two_tmx" : two_tmx, "two_tmn" : two_tmn, 'date' : two_date, 'two_sky' : two_sky}


    return render(request, "home/index.html", {"Rc1": Rc1, "Rc2": Rc2, "Rc3": Rc3, 'val' : val, "sFcst_tbl" : sFcst_tbl, "sNcst_tbl" : sNcst_tbl,
                                               "today_tmx" : today_tmx, "today_tmn" : today_tmn, 'one': one_lst, 'two' : two_lst, 'vFcst_pop':vFcst_pop})