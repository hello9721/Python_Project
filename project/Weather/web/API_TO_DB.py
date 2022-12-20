from datetime import datetime as dt
from datetime import timezone, timedelta
from bs4 import BeautifulSoup as b
import requests as req
import sqlite3 as sql
# lxml 라이브러리 인스톨 하기

from .LOC_TO_XY import *

def get_now():                      # 현재 시간을 필요한 포맷으로 반환
                                    # 데이터를 가져오는 시간에 따라 가장 최근 예보 데이터를 가져올 수 있도록 한다.
    now = dt.now(timezone(timedelta(hours=9)))
    date = now.date()
    time = now.time()

    date = date.strftime("%Y%m%d")
    hour = time.strftime("%H")
    minute = time.strftime("%M")

    sf_hour = hour
    sn_hour = hour

    if int(minute) <= 20: sn_hour = f"{int(sn_hour) - 1:02d}"

    if int(minute) <= 55: sf_hour = f"{int(sf_hour) - 1:02d}"

    return date, sn_hour, sf_hour

def get_tomm():

    now = dt.now()

    tomm1 = now + timedelta(days=1) 
    tomm2 = now + timedelta(days=2)
    
    tomm1 = tomm1.strftime("%Y년 %m월 %d일")
    tomm2 = tomm2.strftime("%Y년 %m월 %d일")

    return tomm1, tomm2 

    # gf_hour = 단기예보는 예보시간이 정해져있고 그 시간 + 10 분에 업데이트 되기에 업데이트 되기전이라면 전시간을 반환
    # sn_hour = 초단기 실황은 예보시간이 정각이고 + 10 분에 업데이트 되기에 업데이트 되기전이라면 시간을 -1 하여 반환
    # sf_hour = 초단기예보 예보시간은 단기예보나 초단기실황과 달리 정각이 아니기에 기준을 +35 분으로 잡아 따로 반환

# cst --------> vFcst = 단기예보 / sFcst = 초단기예보 / sNcst = 초단기실황

def get_data(cst, ad_thr):                         # api에서 데이터 가져오기

    date, sn_time, sf_time = get_now()

    api_key = "%2FsB%2B4nyywlmejmA0rBxb02w%2BxrxK3P17tIQb5iDWiPsMOB1Hzpm%2BvNDN%2BYg2pBtldu9aDkNHZ9N9KKGGgf6BCw%3D%3D"

    address = ""
    x, y = 0, 0

    if type(ad_thr) == dict:                        # ip 주소로 조회 시 ad_thr 가 {'ip' : ip} 형식으로 들어옴

        lat, lng = ip_to_loc(ad_thr['ip'])          # ip 주소에 따른 위도, 경도 값 받아오기
        address, x, y = loc_to_xy(lat, lng)         # 주소, x, y 값 받아오기
                                                    # 요청된 cst에 따라 api에서 가져오는 데이터가 다르도록 지정.        
    elif type(ad_thr) == str:                       # 지역 주소로 조회 시 ad_thr 가 문자열로 들어옴

        x, y = ad_to_xy(ad_thr)

    if cst == "vFcst": url = f"https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={api_key}&pageNo=1&numOfRows=1000&dataType=XML&base_date={date}&base_time=0500&nx={x}&ny={y}"
    elif cst == "sFcst": url = f"https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?serviceKey={api_key}&pageNo=1&numOfRows=1000&dataType=XML&base_date={date}&base_time={sf_time + '30'}&nx={x}&ny={y}"
    elif cst == "sNcst": url = f"https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey={api_key}&pageNo=1&numOfRows=1000&dataType=XML&base_date={date}&base_time={sn_time + '00'}&nx={x}&ny={y}"

    result = req.get(url, verify = False)
    soup = b(result.text, 'lxml')

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

    return lst, address                             # 전체 리스트 반환


def data_to_DB(lst, cst):                           # 리스트 형식으로 들어온 데이터를 DB에 저장

    con = sql.connect("Weather_Data.db")            # DB 연결
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
        
        if i[2][0].upper() == "VEC":

            vec_lst = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']
            vec = int((float(i[2][1]) + 22.5 * 0.5) / 22.5)

            idx = vec_lst[vec]
            query = f'UPDATE {cst} SET {i[2][0]} = "{idx}" WHERE Datetime = "{i[0]} {i[1]}"'

        if i[2][0].upper() == 'SKY':

            sky_lst = ['sunny', 'sunny', 'cloudy', 'cloudy', 'cloud']
            sky = int(i[2][1])
            
            idx = sky_lst[sky]
            query = f'UPDATE {cst} SET {i[2][0]} = "{idx}" WHERE Datetime = "{i[0]} {i[1]}"'

        if i[2][0].upper() == 'PTY':

            pty_lst = ['-', '비', '비/눈', '눈', '소나기', '빗방울', '빗방울/눈날림', '눈날림']
            pty = int(i[2][1])
            
            idx = pty_lst[pty]
            query = f'UPDATE {cst} SET {i[2][0]} = "{idx}" WHERE Datetime = "{i[0]} {i[1]}"'

        cmd.execute(query)
        cmd.fetchall()
        con.commit()