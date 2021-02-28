import requests
from bs4 import BeautifulSoup
import inquire_all_station as ias
import bus_tools as bt

# 춘천시 도시번호 32010

url = 'http://openapi.tago.go.kr/openapi/service/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList'
p_key = ias.init_bus.p_key
p_city = ias.init_bus.p_city


def search_station(entered):  
    ids = dict(filter(lambda item: entered in item[1][0], ias.station_dict.items()))
    # ids = [key:val for key, val in iar.bus_dict.items() if entered in key] 
    res = ''
    #print(ids)
    for key,val in ids.items():
        res += "\n [ " + key + " ] " + val[0] + "\n- "
        bus = get_station_status(val[1])
        if bus:
            res += '\n- '.join(bus) + "\n"
        else:
            res += "배차 정보가 없습니다.\n"
    print(res)
    return res

def get_station_status (node_id):

    #print(node_id)
    res = requests.get(url+'?'+p_key+'&'+p_city+'&'+'nodeId='+node_id)
    res_parse = BeautifulSoup(res.text,"html.parser")
    ret=[]
    
    arr_bus_no = bt.remove_tags(res_parse.find_all("routeno"))
    arr_bus_time = bt.remove_tags(res_parse.find_all("arrtime"))
    
    for key,val in dict(zip(arr_bus_no,arr_bus_time)).items():
        ret.append(key + " [ " + str(int(val)/60) + " 분]" )
        
    #print(ret)
    return ret        
        
# print(get_station_status('1671'))
# search_station("강원대후문")    
    