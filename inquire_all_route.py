import requests
from bs4 import BeautifulSoup
import initialize as init_bus
import bus_tools as bt

# 춘천시 도시번호 32010

url = 'http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/getRouteNoList'

p_route_num = init_bus.get_route_rows()
res = requests.get(url+'?'+init_bus.p_key+'&'+init_bus.p_city+'&numOfRows='+p_route_num)
res_parse = BeautifulSoup(res.text,"html.parser")


route_name_list = bt.remove_tags(res_parse.find_all("routeno"))
route_id_list = bt.remove_tags(res_parse.find_all("routeid"))
                         
bus_dict = dict(zip(route_name_list,route_id_list))

# print(bus_dict)
    