# from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from datetime import datetime, time
from urllib.request import urlopen, Request
import urllib



def menu_school_cafeteria(cafeteria,date,mealtime):
    
    print(cafeteria)
    print(date)
    print(mealtime)
    
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
    
    # 날짜를 숫자로 매핑
    if today < 5:
        if date == "오늘" and int_time_now <= 2399:
            day = today % 5
        elif date == "오늘" and int_time_now >= 2400:
            day = (today + 1) % 5
        elif date == "내일" and int_time_now <= 2399:
            day = (today + 1) % 5
        elif date == "내일" and int_time_now >= 2400:
            day = (today + 2) % 5
    else:
        if int_time_now <= 2399:
            day = today
        else:
            day = today + 1
      
    # 요일 문자열을 숫자로 매핑
    if date in ["월요일", "화요일", "수요일", "목요일", "금요일"]:
        tday = {"월요일":0, "화요일":1, "수요일":2, "목요일":3, "금요일":4}
        day = tday[date]
    print(day)
   
    # 천지관일때
    if cafeteria == "천지관":
        url = 'https://www.kangwon.ac.kr/www/selecttnCafMenuListWU.do?key=1077&sc1=CC10&sc2=CC'
        req = Request(url)
        page = urlopen(req)
        html = page.read()
        page.close()
    
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        table = tables[1]
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        
        # 식사시간이 default_value일때 백반,특식 아점저 + 고정메뉴 출력
        if mealtime == "default_value":
            answer = ""
            # 주말이 아니면
            if day < 5:
                # 백반,특식 아점저
                for tr in trs:
                    ths = tr.find_all('th')
                    for th in ths:
                        if th.text in ["백반", "특식", "뚝배기(더진국)"]:
                            th_foodtype = th.text
                            print(th_foodtype)
                        if th.text in ["아침", "점심", "저녁"]:
                            th_mealtime = th.text
                    if th_foodtype in ["백반", "특식"]:
                        rest_val = str(tr.select("td")[day]).replace("<td>", " - ").replace("</td>", "").replace("<br/>", "\n - ").replace("&amp;", " & ")
                        answer = answer + "< " + cafeteria + " " + th_foodtype + " " + th_mealtime + " 메뉴 >\n" + rest_val + "\n\n"
                    else:
                        break;
                # 고정메뉴
                answer = answer + " * 고정메뉴 : 더진국(뚝배기)\n - 수육국밥\n - 순대국밥\n - 얼큰국밥\n - 옛날전통순대"
                answer = answer + "\n\n * 고정메뉴 : 돈까스\n - 통등심돈까스\n - 치즈돈까스\n - 고구마치즈돈까스\n - 수제치킨까스\n - 돈까스정식\n - 함박정식\n - 눈꽃치즈돈까스\n - 왕돈까스"
                answer = answer + "\n\n * 고정메뉴 : 라면\n - 라면\n - 떡만두라면\n - 치즈라면\n - 해장라면&공기밥\n - 스팸라면\n - 가락우동\n - 꼬치어묵우동\n - 새우튀김우동\n - 잔치국수"
            
            # 주말일때 응답처리
            else:
                answer = " < " + cafeteria + " " + date + " " + " 메뉴 >\n"
                answer = "\n ★ 주말엔 운영하지 않습니다 ~ ★\n"
                
            answer = answer + "\n\n" + "* 평일 : 08:00 ~ 19:00 \n* 토요일, 일요일, 공휴일 휴무"
        
        # 식사시간과 요일이 모두 주어졌을 때 특정시간메뉴 + 고정메뉴 출력
        else:
            if mealtime == "아침":
                stime = {"백반":0}
            elif mealtime == "점심":
                stime = {"백반":1, "특식":3}
            elif mealtime == "저녁":
                stime = {"백반":2, "특식":4}
            
            answer = " < " + cafeteria + " " + date + " " + mealtime + " 메뉴 >\n"
            # 주말이 아니면
            if day < 5:
                for time in stime.items():
                    print(time)
                    print(type(time))
                    print(stime)
                    rest_val = str(trs[time[1]].select("td")[day]).replace("<td>", " - ").replace("</td>", "").replace("<br/>", "\n - ").replace("&amp;", " & ")
                    answer = answer + " * " + time[0] + " " + " 메뉴\n" + rest_val + "\n\n" 
                # 고정메뉴 출력
                answer = answer + " * 고정메뉴 : 더진국(뚝배기)\n - 수육국밥\n - 순대국밥\n - 얼큰국밥\n - 옛날전통순대"
                answer = answer + "\n\n * 고정메뉴 : 돈까스\n - 통등심돈까스\n - 치즈돈까스\n - 고구마치즈돈까스\n - 수제치킨까스\n - 돈까스정식\n - 함박정식\n - 눈꽃치즈돈까스\n - 왕돈까스"
                answer = answer + "\n\n * 고정메뉴 : 라면\n - 라면\n - 떡만두라면\n - 치즈라면\n - 해장라면&공기밥\n - 스팸라면\n - 가락우동\n - 꼬치어묵우동\n - 새우튀김우동\n - 잔치국수"
            else:
                answer = " < " + cafeteria + " " + date + " " + " 메뉴 >\n"
                answer = answer + "\n ★ 주말엔 운영하지 않습니다 ~ ★\n"
            answer = answer + "\n * 평일 : 08:00 ~ 19:00 \n* 토요일, 일요일, 공휴일 휴무"
    
    # 백록관일때
    elif cafeteria == "백록관":
        url = 'https://www.kangwon.ac.kr/www/selecttnCafMenuListWU.do?key=1077&sc1=CC20&sc2=CC'
        req = Request(url)
        page = urlopen(req)
        html = page.read()
        page.close()
    
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        table = tables[1]
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        
        # 식사시간이 default_value일때 백반,특식 점저 + 고정메뉴 출력
        if mealtime == "default_value":
            answer = ""
            # 주말이 아니면
            if day < 5:
                # 백반,특식 점저
                for tr in trs:
                    ths = tr.find_all('th')
                    for th in ths:
                        if th.text in ["백반", "특식", "뚝배기(더진국)"]:
                            th_foodtype = th.text
                            print(th_foodtype)
                        if th.text in ["점심", "저녁"]:
                            th_mealtime = th.text
                    if th_foodtype in ["백반", "특식"]:
                        rest_val = str(tr.select("td")[day]).replace("<td>", " - ").replace("</td>", "").replace("<br/>", "\n - ").replace("&amp;", " & ")

                        answer = answer + "< " + cafeteria + " " + th_foodtype + " " + th_mealtime + " 메뉴 >\n" + rest_val + "\n\n"
                    else:
                        break;
                # 고정메뉴
                answer = answer + " * 고정메뉴 : 더진국(뚝배기)\n - 수육국밥\n - 순대국밥\n - 얼큰국밥\n - 옛날전통순대"
                answer = answer + "\n\n * 고정메뉴 : 돈까스\n - 통등심돈까스\n - 치즈돈까스\n - 트윈돈까스\n - 수제치킨까스\n - 피자돈까스\n - 백록함박까스\n - 베오베돈까스"
                answer = answer + "\n\n * 고정메뉴 : 라면\n - 라면\n - 떡만두라면\n - 치즈라면\n - 해장라면&공기밥\n - 백점뽈라면\n - 마라면\n - 가락우동\n - 꼬치어묵우동\n - 돈카츠우동\n - 호로록잔치국수"
            
            # 주말일때 응답처리
            else:
                answer = " < " + cafeteria + " " + date + " " + " 메뉴 >\n"
                answer = "\n ★ 주말엔 운영하지 않습니다 ~ ★\n"
                
            answer = answer + "\n\n" + "* 평일 : 08:00 ~ 19:00 \n * 토요일, 일요일, 공휴일 휴무"
        
        # 식사시간과 요일이 모두 주어졌을 때 특정시간메뉴 + 고정메뉴 출력
        else:
            if mealtime == "점심":
                stime = {"백반":0, "특식":2}
            elif mealtime == "저녁":
                stime = {"백반":1, "특식":3}
            answer = " < " + cafeteria + " " + date + " " + mealtime + " 메뉴 >\n"
            # 주말이 아니면
            if day < 5:
                for time in stime.items():
                    print(time)
                    print(type(time))
                    print(stime)
                    rest_val = str(trs[time[1]].select("td")[day]).replace("<td>", " - ").replace("</td>", "").replace("<br/>", "\n - ").replace("&amp;", " & ")
                    answer = answer + " * " + time[0] + " " + " 메뉴\n" + rest_val + "\n\n" 
                # 고정메뉴
                answer = answer + " * 고정메뉴 : 더진국(뚝배기)\n - 수육국밥\n - 순대국밥\n - 얼큰국밥\n - 옛날전통순대"
                answer = answer + "\n\n * 고정메뉴 : 돈까스\n - 통등심돈까스\n - 치즈돈까스\n - 고구마치즈돈까스\n - 수제치킨까스\n - 돈까스정식\n - 함박정식\n - 눈꽃치즈돈까스\n - 왕돈까스"
                answer = answer + "\n\n * 고정메뉴 : 라면\n - 라면\n - 떡만두라면\n - 치즈라면\n - 해장라면&공기밥\n - 스팸라면\n - 가락우동\n - 꼬치어묵우동\n - 새우튀김우동\n - 잔치국수"
                
            else:
                answer = " < " + cafeteria + " " + date + " " + " 메뉴 >\n"
                answer = answer + "\n ★ 주말엔 운영하지 않습니다 ~ ★\n"
                
            answer = answer + "\n * 평일 : 10:00 ~ 19:00 \n * 토요일, 일요일, 공휴일 휴무\n * 백록관 백반은 아침식사가 없습니다"
    
    # 교직원 일때
    elif cafeteria == "교직원":
        url = 'https://www.kangwon.ac.kr/www/selecttnCafMenuListWU.do?key=1077&sc1=CC30&sc2=CC'
        req = Request(url)
        page = urlopen(req)
        html = page.read()
        page.close()
    
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        table = tables[1]
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        
        answer = " < 교직원 식당 " + date + " 점심 메뉴 >\n" 

        # 주말이 아니면
        if day < 5:
            # 백록관,천지관 교직원 점심
            for tr in trs:
                ths = tr.find_all('th')
                for th in ths:
                    if th.text in ["천지관 교직원식당", "백록관 교직원식당"]:
                        th_foodtype = th.text
                        print(th_foodtype)
                    if th.text in ["점심"]:
                        th_mealtime = th.text
                    rest_val = str(tr.select("td")[day]).replace("<td>", " - ").replace("</td>", "").replace("<br/>", "\n - ").replace("&amp;", " & ")
                answer = answer + " * " + th_foodtype + " " + th_mealtime + " 메뉴\n" + rest_val + "\n\n" 
        else:
            answer = " < " + cafeteria + " " + date + " " + " 메뉴 >\n"
            answer = answer + "\n ★ 주말엔 운영하지 않습니다 ~ ★\n"

        answer = answer + "\n * 평일 : 11:30 ~ 13:30 \n * 토요일, 일요일, 공휴일 휴무\n * 교직원 식당은 점심시간만 운영합니다"
    
    # res = {
    #     "version": "2.0",
    #     "template": {
    #         "outputs": [
    #             {
    #                 "simpleText": {
    #                     "text": answer

    #                 }
    #             }
    #         ]
    #     }
    # }
    return answer
    

#메인 함수
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, threaded=True)


