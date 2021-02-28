import requests
from bs4 import BeautifulSoup
import bus_tools as bt

url = "https://www.kangwon.ac.kr/www/selectTnSchafsSchdulListUS.do;jsessionid=93A0BF87EB878A6DB0F35E701AB9AF93?ti1=2019&si1=2020&sc1=%ED%95%99%EC%82%AC%EC%9D%BC%EC%A0%95&sc2=TERMSCH&sc5=20200101&sc6=20201231&ad1=0&key=156"

res = requests.get(url)
res_parse = BeautifulSoup(res.text,"html.parser")

def get_calendar(month):
    
    tmp = res_parse.find_all(id="month"+str(month)).find_all(class_="skip")
    
    
    print(bt.remove_tags(tmp))
    
get_calendar(12)