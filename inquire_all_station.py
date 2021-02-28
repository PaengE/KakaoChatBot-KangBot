import requests
from bs4 import BeautifulSoup
import initialize as init_bus
import bus_tools as bt

# 춘천시 도시번호 32010

url = 'http://openapi.tago.go.kr/openapi/service/BusSttnInfoInqireService/getSttnNoList'
p_key = init_bus.p_key
p_city = init_bus.p_city

p_station_num = init_bus.get_station_rows()

res = requests.get(url+'?'+p_key+'&'+p_city+'&numOfRows='+p_station_num)
res_parse = BeautifulSoup(res.text,"html.parser")

station_name_list = bt.remove_tags(res_parse.find_all("nodenm"))
station_no_list = bt.remove_tags(res_parse.find_all("nodeno"))
station_id_list = bt.remove_tags(res_parse.find_all("nodeid"))

station_info = [] 

for i in range(0,int(init_bus.get_station_rows())):
    station_info.append([station_name_list[i],station_id_list[i]])
    station_dict = dict(zip(station_no_list,station_info))

                         
#print (station_list)
#print(station_dict)
#print(station_dict.items())    