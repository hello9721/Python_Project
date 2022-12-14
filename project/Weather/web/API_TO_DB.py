from datetime import datetime as dt
from bs4 import BeautifulSoup as b
import requests as req
import sqlite3 as sql
# lxml 라이브러리 인스톨 하기

from LOC_TO_XY import *

def get_now():                      # 현재 시간을 필요한 포맷으로 반환
                                    # 데이터를 가져오는 시간에 따라 가장 최근 예보 데이터를 가져올 수 있도록 한다.
    now = dt.now()
    date = now.date()
    time = now.time()

    date = date.strftime("%Y%m%d")
    hour = time.strftime("%H")
    minute = time.strftime("%M")

    gf_lst = [2, 5, 8, 11, 14, 17, 20, 23]

    sf_hour = hour
    sn_hour = hour
    gf_hour = hour
    gf_idx = 0
    
    for i in range(len(gf_lst)):

        if int(gf_hour) >= gf_lst[i] : gf_idx = i
        elif int(gf_hour) == 00 : gf_idx = len(gf_lst) - 1

    if int(minute) <= 10:
        
        sn_hour = f"{int(sn_hour) - 1:02d}"
        gf_idx -= 1

    if int(minute) <= 45: sf_hour = f"{int(sf_hour) - 1:02d}"

    gf_hour = f"{gf_lst[gf_idx]:02d}"

    return date, gf_hour, sn_hour, sf_hour

    # gf_hour = 단기예보는 예보시간이 정해져있고 그 시간 + 10 분에 업데이트 되기에 업데이트 되기전이라면 전시간을 반환
    # sn_hour = 초단기 실황은 예보시간이 정각이고 + 10 분에 업데이트 되기에 업데이트 되기전이라면 시간을 -1 하여 반환
    # sf_hour = 초단기예보 예보시간은 단기예보나 초단기실황과 달리 정각이 아니기에 기준을 +35 분으로 잡아 따로 반환

# cst --------> vFcst = 단기예보 / sFcst = 초단기예보 / sNcst = 초단기실황

def get_data(cst, ad_thr):                         # api에서 데이터 가져오기

    date, gf_time, sn_time, sf_time = get_now()

    api_key = "%2FsB%2B4nyywlmejmA0rBxb02w%2BxrxK3P17tIQb5iDWiPsMOB1Hzpm%2BvNDN%2BYg2pBtldu9aDkNHZ9N9KKGGgf6BCw%3D%3D"

    address = ""
    x, y = 0, 0

    if ad_thr == '':

        lat, lng = ip_to_loc()                      # ip 주소에 따른 위도, 경도 값 받아오기
        address, x, y = loc_to_xy(lat, lng)         # 주소, x, y 값 받아오기
                                                    # 요청된 cst에 따라 api에서 가져오는 데이터가 다르도록 지정.        
    elif ad_thr != '':

        x, y = ad_to_xy(ad_thr)

    if cst == "vFcst": url = f"https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={api_key}&pageNo=1&numOfRows=1000&dataType=XML&base_date={date}&base_time={gf_time + '00'}&nx={x}&ny={y}"
    elif cst == "sFcst": url = f"https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?serviceKey={api_key}&pageNo=1&numOfRows=1000&dataType=XML&base_date={date}&base_time={sf_time + '30'}&nx={x}&ny={y}"
    elif cst == "sNcst": url = f"https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey={api_key}&pageNo=1&numOfRows=1000&dataType=XML&base_date={date}&base_time={sn_time + '00'}&nx={x}&ny={y}"

    result = req.get(url, verify = False)
    soup = b(result.text, 'lxml')

    print(address)                                  # 추후 주소 사용할때 수정할 부분

    items = soup.find_all('item')

    lst = []

    for i in items:

        Date = i.find('basedate').get_text()        # 예보 발표 날짜
        Time = i.find('basetime').get_text()        # 예보 발표 시간
        category = i.find('category').get_text()    # 예보 항목
        Value = ""

        if (cst == "vFcst") or (cst == "sFcst"):    # 초단기예보, 단기예보에만 예보가 있기에 예보값 추출
            
            Date = i.find('fcstdate').get_text()    # 예보 날짜
            Time = i.find('fcsttime').get_text()    # 예보 시간
            Value = i.find('fcstvalue').get_text()  # 예보 값
        
        elif cst == "sNcst": Value = i.find('obsrvalue').get_text()
                                                    # 초단기실황은 따로 관측값 추출

        if (Value == '강수없음')  or (Value == '적설없음'): Value = "-"
                                                    # 강수없음, 적설없음은 - 로 표시

        temp = [Date, Time, [category, Value]]      # 리스트 형식으로 저장

        lst.append(temp)

    return lst                                      # 전체 리스트 반환


def data_to_DB(lst, cst):                           # 리스트 형식으로 들어온 데이터를 DB에 저장

    con = sql.connect("..\Weather_Data.db")         # DB 연결
    cmd = con.cursor()

    if cst == "vFcst": cst = "VilageFcst"           # cst별 테이블 다르게
    elif cst == "sFcst": cst = "SrtFcst"
    elif cst == "sNcst": cst = "SrtNcst"
    
    query = f"DELETE FROM {cst}"                    # 이전 기록 초기화
    
    cmd.execute(query)
    cmd.fetchall()
    con.commit()

    for i in lst:                                   # 리스트에서 하나씩 가져오면서 중복되지 않게 날짜/시간 넣기

        try:

            query = f'INSERT INTO {cst}(Datetime) VALUES ("{i[0]} {i[1]}")'

            cmd.execute(query)
            cmd.fetchall()
            con.commit()

        except: continue

    for i in lst:                                   # 다시 리스트에서 하나씩 가져오면서 해당 날짜/시간 데이터 행의 항목 값 넣기

        query = f'UPDATE {cst} SET {i[2][0]} = "{i[2][1]}" WHERE Datetime = "{i[0]} {i[1]}"'

        cmd.execute(query)
        cmd.fetchall()
        con.commit()

# 테스트 실행 코드
# vFcst = 단기예보 / sFcst = 초단기예보 / sNcst = 초단기실황

# vf_lst = get_data('vFcst')
# sf_lst = get_data('sFcst')
# sn_lst = get_data('sNcst')

# data_to_DB(vf_lst, 'vFcst')
# data_to_DB(sf_lst, 'sFcst')
# data_to_DB(sn_lst, 'sNcst')