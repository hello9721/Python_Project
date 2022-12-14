import json
import random as rd
import requests
import sqlite3 as sql

def ip_to_loc():                                    # Google Geolocation API 를 이용하여 접속 IP의 위도, 경도를 반환하는 함수

    api_key = "AIzaSyCxUJvUYcT-DO2xIbsatBmp6gEW2WAE9eY"

    LOCATION_API_KEY = api_key

    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={LOCATION_API_KEY}'
    data = {
        'considerIp': True,
    }

    result = requests.post(url, data)

    loc = json.loads(result.text)                   # 받아온 결과를 json 형태 (dict 형태) 로 변환
    loc = loc["location"]

    lat = f"{loc['lat']:.2f}"                       # 위도
    lng = f"{loc['lng']:.2f}"                       # 경도

    return lat, lng                                 # 반환

def loc_to_xy(lat, lng):                            # 들어온 위도, 경도를 통해 지역정보DB에서 주소, x, y를 가져오는 함수

    con = sql.connect("..\Location.db")
    cmd = con.cursor()

    query = f"SELECT ONE, TWO, THR, X, Y FROM location WHERE LAT = '{lat}' AND LNG = '{lng}'"
    cmd.execute(query)
    
    data = cmd.fetchall()
    if len(data) > 1: data = rd.choice(data)        # 결과가 1개 이상일 때 무작위로 하나 추출 -------> () 형태
    else: data = data[0]                            # 무작위 과정을 거치지 않은 data는 [()] 형태이므로 () 형태로 바꿔 데이터 형식을 맞춰준다. 

    location = data[0], data[1], data[2]            # 위치 주소 정보 ( 튜플 형태로 저장 )
    x, y = data[3], data[4]                         # x, y 값

    return location, x, y

def ad_to_xy(three):

    con = sql.connect("..\Location.db")
    cmd = con.cursor()

    query = f"SELECT X, Y LOCATION WHERE THR = '{three}'"
    cmd.execute(query)
    
    data = cmd.fetchall()
    data = data[0]

    x, y = data[0], data[1]

    return x, y