import requests
from bs4 import BeautifulSoup

# 춘천시 도시번호 32010


p_city = 'cityCode=32010'
p_key = 'serviceKey=0N%2FaSVpDUOf4p8up3V2LCtqtwGD0yaY892VYGDqGTSx56lpXCJMrxdsSoCC55HNp6RamQlMHIUBGsufmqDdEeQ%3D%3D'

def get_route_rows() :
    
    url = 'http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/getRouteNoList'
    
    res = requests.get(url+'?'+p_key+'&'+p_city)
    res_parse = BeautifulSoup(res.text,"html.parser")
    tot_route = res_parse.body.totalcount.get_text()
    return tot_route

def get_station_rows() :
    
    url = 'http://openapi.tago.go.kr/openapi/service/BusSttnInfoInqireService/getSttnNoList'
    
    res = requests.get(url+'?'+p_key+'&'+p_city)
    res_parse = BeautifulSoup(res.text,"html.parser")
    tot_station = res_parse.body.totalcount.get_text()
    return tot_station

# print(get_station_rows())
