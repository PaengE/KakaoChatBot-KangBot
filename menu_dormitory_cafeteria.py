from bs4 import BeautifulSoup
from datetime import datetime, time
from urllib.request import urlopen, Request
import urllib

def menu_dormitory_cafeteria(cafeteria,date,mealtime):
    
    
    # print(cafeteria)
    # print(date)
    # print(mealtime)
    
    # 요일 문자열을 숫자로 매핑
    if date in ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]:
        tday = {"월요일":1, "화요일":2, "수요일":3, "목요일":4, "금요일":5, "토요일":6, "일요일":7}
        day = tday[date]
        
    # 시간 처리
    now = datetime.now()
    hour = str(now.hour)
    minute = str(now.minute).zfill(2)
    str_time_now = hour + minute
    # 요일 빈문자열 처리
    today = datetime.today().weekday()
    # 한국표준시로 변환
    int_time_now = int(str_time_now) + 900
    print(int_time_now)
    
    if date == "오늘" and int_time_now <= 2399:
        day = (today + 1) % 8
    elif date == "오늘" and int_time_now >= 2400:
        day = (today + 2) % 8
    elif date == "내일" and int_time_now <= 2399:
        day = (today + 2) % 8
    elif date == "내일" and int_time_now >= 2400:
        day = (today + 3) % 8
    
    if day == 0:
        day = day + 1
    print(today)
    print(day)
        
    # 식사시간 문자열을 숫자로 매핑
    if mealtime in ["아침", "점심", "저녁"]:
        ttime = {"아침":0, "점심":1, "저녁":2}
        time = ttime[mealtime]
    elif mealtime == "default_value":
        stime = [0, 1, 2]
    
    url = 'http://knudorm.kangwon.ac.kr/home/sub02/sub02_05_bj.jsp#'
    req = Request(url)
    page = urlopen(req)
    html = page.read()
    page.close()
    soup = BeautifulSoup(html, "html.parser")
    
    if cafeteria == "재정생활관":
        t1 = soup.find('div', id='foodtab1').find('div', id='foodtab1_building1').find('table', class_='table_type01')
        trs1 = t1.find_all('tr')
        ths1 = trs1[0].find_all('th')
        rest_key = str(trs1[day].th.text + "요일")
        tds1 = trs1[day].find_all('td')
        
        # mealtime이 default_value면 아점저 출력
        if mealtime == "default_value":
            answer = " < " + cafeteria + " 식당 " + date + " " + " 메뉴 > \n"
            for time in stime:
                split_value = str(tds1[time].text).split()
                rest_value = str(split_value).replace("['", " - ").replace("', '", "\n - ").replace("']", "")
                answer = answer + " * " + ths1[time+1].text + ":\n" 
                answer = answer + rest_value + "\n\n"
            answer = answer + " * 운영시간 안내 * \n  + [월~금요일] 아침 : 07:30 ~ 09:00,\n  점심 : 11:30 ~ 13:30, 저녁 : 17:30 ~ 19:00\n  * 토, 일, 공휴일은 운영하지 않습니다. :)"
            
        # day와 mealtime이 다 주어졌을 때는 특정 날짜 특정 식사 출력
        else:
            answer = " < " + cafeteria + " 식당 " + date + " " + mealtime + " 메뉴 > \n"
            split_value = str(tds1[time].text).split()
            rest_value = str(split_value).replace("['", " - ").replace("', '", "\n - ").replace("']", "")
            answer = answer + rest_value + "\n\n"
            answer = answer + " * 운영시간 안내 * \n  + [월~금요일] 아침 : 07:30 ~ 09:00,\n  점심 : 11:30 ~ 13:30, 저녁 : 17:30 ~ 19:00\n  * 토, 일, 공휴일은 운영하지 않습니다. :)"
        
        
    elif cafeteria == "새롬관":
        t2 = soup.find('div', id='foodtab2').find_all('table', class_='table_type01')
        trs2 = t2[1].find_all('tr')
        ths2 = trs2[0].find_all('th')
        rest_key = str(trs2[day].th.text + "요일")
        tds2 = trs2[day].find_all('td')
        
        # mealtime이 default_value면 아점저 출력
        if mealtime == "default_value":
            answer = " < " + cafeteria + " 식당 " + date + " " + " 메뉴 > \n"
            for time in stime:
                split_value = str(tds2[time].text).split()
                rest_value = str(split_value).replace("['", " - ").replace("', '", "\n - ").replace("']", "")
                answer = answer + " * " + ths2[time+1].text + ":\n" 
                answer = answer + rest_value + "\n\n"
            answer = answer + " * 운영시간 안내 * \n  + [월~금요일] 아침 : 08:00 ~ 09:00,\n  점심 : 11:30 ~ 13:30, 저녁 : 17:00 ~ 18:30\n  + [토, 일, 공휴일] 아침 : 08:00 ~ 09:00,\n  점심 : 12:00 ~ 13:00, 저녁 : 17:30 ~ 18:30"
        
        # day와 mealtime이 다 주어졌을 때는 특정 날짜 특정 식사 출력
        else:
            answer = " < " + cafeteria + " 식당 " + date + " " + mealtime + " 메뉴 > \n"
            split_value = str(tds2[time].text).split()
            rest_value = str(split_value).replace("['", " - ").replace("', '", "\n - ").replace("']", "")
            answer = " < " + cafeteria + " 식당 " + date + " " + mealtime + " 메뉴 > \n"
            answer = answer + rest_value + "\n\n"
            answer = answer + " * 운영시간 안내 * \n  + [월~금요일] 아침 : 08:00 ~ 09:00,\n  점심 : 11:30 ~ 13:30, 저녁 : 17:00 ~ 18:30\n  + [토, 일, 공휴일] 아침 : 08:00 ~ 09:00,\n  점심 : 12:00 ~ 13:00, 저녁 : 17:30 ~ 18:30"
        
        
    elif cafeteria == "이룸관":
        t3 = soup.find('div', id='foodtab3').find_all('table', class_='table_type01')
        trs3 = t3[1].find_all('tr')
        ths3 = trs3[0].find_all('th')
        rest_key = str(trs3[day].th.text + "요일")
        tds3 = trs3[day].find_all('td')
        
        # mealtime이 default_value면 아점저 출력
        if mealtime == "default_value":
            answer = " < " + cafeteria + " 식당 " + date + " " + " 메뉴 > \n"
            for time in stime:
                split_value = str(tds3[time].text).split()
                rest_value = str(split_value).replace("['", " - ").replace("', '", "\n - ").replace("']", "")
                answer = answer + " * " + ths3[time+1].text + ":\n" 
                answer = answer + rest_value + "\n\n"
            answer = answer + " * 운영시간 안내 * \n  + [월~금요일] 아침 : 08:00 ~ 09:00,\n  점심 : 11:30 ~ 13:30, 저녁 : 17:00 ~ 18:30\n  + [토, 일, 공휴일] 아침 : 08:00 ~ 09:00,\n  점심 : 12:00 ~ 13:00, 저녁 : 17:30 ~ 18:30"
            
        # day와 mealtime이 다 주어졌을 때는 특정 날짜 특정 식사 출력
        else:
            answer = " < " + cafeteria + " 식당 " + date + " " + mealtime + " 메뉴 > \n"
            split_value = str(tds3[time].text).split()
            rest_value = str(split_value).replace("['", " - ").replace("', '", "\n - ").replace("']", "")
            answer = " < " + cafeteria + " 식당 " + date + " " + mealtime + " 메뉴 > \n"
            answer = answer + rest_value + "\n\n"
            answer = answer + " * 운영시간 안내 * \n  + [월~금요일] 아침 : 08:00 ~ 09:00,\n  점심 : 11:30 ~ 13:30, 저녁 : 17:00 ~ 18:30\n  + [토, 일, 공휴일] 아침 : 08:00 ~ 09:00,\n  점심 : 12:00 ~ 13:00, 저녁 : 17:30 ~ 18:30"
            
    answer = answer + "\n\n * 원산지 * \n  + 국내산 : 돼지고기, 닭고기, 쌀(밥, 누룽지, 죽), 콩국수, 고등어\n  + 수입산 : 두부류, 콩비지, 갈치, 꽃게, 낙지, 명태, 오징어, 참조기\n  + 호주산 : 소고기\n  + 미국산 : 닭다리, 닭갈비"
   
    return answer
    

# #메인 함수
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, threaded=True)
