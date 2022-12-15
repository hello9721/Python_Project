import json
import random as rd
import requests as req
import sqlite3 as sql


def get_ip(request):                                # 현재 GET 요청을 한 IP 주소 추출

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context = {'ip' : ip}

    return context

# def ip_to_loc(ip):                                  # https://ip-api.com/docs/api:json 를 이용하여 입력 IP의 위도, 경도를 반환하는 함수 (배포용)
    
#     url = f'http://ip-api.com/json/{ip}?fields=lat,lon'

#     result = req.get(url, verify = False)

#     loc = json.loads(result.text)                   # 받아온 결과를 json 형태 (dict 형태) 로 변환

#     lat = f"{loc['lat']:.2f}"                       # 위도
#     lng = f"{loc['lon']:.2f}"                       # 경도

#     return lat, lng                                 # 반환

def ip_to_loc(ip):                                  # Google Geolocation API 를 이용하여 접속 IP의 위도, 경도를 반환하는 함수 (로컬용)
                                                    # 현재 서버 컴퓨터의 IP를 통해 위도, 경도가 나오기 때문에 로컬에서만 실행
                                                    
    api_key = "AIzaSyCxUJvUYcT-DO2xIbsatBmp6gEW2WAE9eY"

    LOCATION_API_KEY = api_key

    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={LOCATION_API_KEY}'
    data = {
        'considerIp': True,
    }

    result = req.post(url, data)

    loc = json.loads(result.text)                   # 받아온 결과를 json 형태 (dict 형태) 로 변환
    loc = loc["location"]

    lat = f"{loc['lat']:.2f}"                       # 위도
    lng = f"{loc['lng']:.2f}"                       # 경도

    return lat, lng                                 # 반환

def loc_to_xy(lat, lng):                            # 들어온 위도, 경도를 통해 지역정보DB에서 주소, x, y를 가져오는 함수

    con = sql.connect("Location.db")
    cmd = con.cursor()

    query = f"SELECT ONE, TWO, THR, X, Y FROM location WHERE LAT = '{lat}' AND LNG = '{lng}'"
    cmd.execute(query)
    
    data = cmd.fetchall()
    if len(data) > 1: data = rd.choice(data)        # 결과가 1개 이상일 때 무작위로 하나 추출 -------> () 형태
    else: data = data[0]                            # 무작위 과정을 거치지 않은 data는 [()] 형태이므로 () 형태로 바꿔 데이터 형식을 맞춰준다. 

    location = data[0], data[1], data[2]            # 위치 주소 정보 ( 튜플 형태로 저장 )
    x, y = data[3], data[4]                         # x, y 값

    return location, x, y

def ad_to_xy(three):                                # three 로 마지막 요소의 주소값이 들어오면 그 값으로 x, y 값을 찾아 반환

    con = sql.connect("Location.db")
    cmd = con.cursor()

    query = f"SELECT X, Y FROM LOCATION WHERE THR = '{three}'"
    cmd.execute(query)
    
    data = cmd.fetchall()
    data = data[0]                                  # data = [( x, y )] -> data = (x, y)

    x, y = data[0], data[1]

    return x, y