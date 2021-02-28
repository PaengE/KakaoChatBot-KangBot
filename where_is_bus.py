import requests
from bs4 import BeautifulSoup
import inquire_all_route as iar
import bus_tools as bt

# 춘천시 도시번호 32010

url = 'http://openapi.tago.go.kr/openapi/service/BusLcInfoInqireService/getRouteAcctoBusLcList'
p_key = iar.init_bus.p_key
p_city = iar.init_bus.p_city

def get_bus_location (route_id):

    #print(route_id)
    res = requests.get(url+'?'+p_key+'&'+p_city+'&'+'routeId='+route_id)
    res_parse = BeautifulSoup(res.text,"html.parser")
    ret = []
    for key,val in dict(zip(bt.remove_tags(res_parse.find_all("nodenm")),bt.remove_tags(res_parse.find_all("vehicleno")))).items():
        ret.append(key + " [" + val + "]" )
    return ret
    
def search_bus (entered):  
    ids=dict(filter(lambda item: entered in item[0], iar.bus_dict.items()))
    # ids = [key:val for key, val in iar.bus_dict.items() if entered in key] 
    res=''
    #print(ids)
    for key,val in ids.items():
        res += "\n" + key + "\n- "
        loc = get_bus_location(val)
        if loc:
            res += '\n- '.join(loc) + "\n"
        else:
            res += "배차 정보가 없습니다.\n"
        # print (res)
    return res
    
    
#print(search_bus('서면'))
        

#print (get_bus_location("300"))
#print (get_bus_location("100"))


