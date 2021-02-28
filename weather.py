from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib

# @app.route('/weather', methods=['POST'])
def weather(location,date):

    enc_loc = urllib.parse.quote(location + '+ 날씨')
    el = str(enc_loc)
    url = 'https://search.naver.com/search.naver'
    url = url + '?sm=top_hty&fbm=1&ie=utf8&query='
    url = url + el

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    page.close()
    
    print(location)
    print(date)
    
    # 상세위치
    soup = BeautifulSoup(html, 'html.parser')
    loc1 = soup.find('div', class_='sort_box _areaSelectLayer')
    loc2 = loc1.find('div', class_='lst_select')
    loc3 = loc2.find('div', class_='select_box')
    detail_location = loc3.em.text
    
    # 오늘날씨
    if date == "오늘":
        t= soup.find('div', class_='today_area _mainTabContent').find('div', class_='main_info').find('div', class_='info_data')
        # 현재온도
        current_temperature = t.find('p', class_='info_temperature').find('span', class_='todaytemp').text
        
        # 최저, 최고, 체감온도, 자외선지수
        t1 = t.find('ul', class_='info_list')
        t2 = t1.find('span', class_='merge').find('span', class_='min').find('span', class_='num')
        min_temperature = t2.text
        t3 = t1.find('span', class_='merge').find('span', class_='max').find('span', class_='num')
        max_temperature = t3.text
        t4 = t1.find('span', class_='sensible').find('span', class_='num')
        sensible_temperature = t4.text
        t5 = t1.find('span', class_='lv1')
        ultraviolet = t5.text
        
        # 미세먼지, 초미세먼지, 오존지수
        s = soup.find('div', class_='sub_info').find('div', class_='detail_box').find('dl', class_='indicator')
        s1 = s.find_all('dd')
        fine_dust = s1[0].text
        ultra_fine_dust = s1[1].text
        ozone_index = s1[2].text
        
        # 평균강수확률, 강수량합, 현재시간, 현재시간+4번쨰 블록시간
        u = soup.find('div', class_='table_info bytime _todayWeatherByTime').find('div', class_='info_list rainfall _tabContent').find('ul', class_='list_area')
        lis = u.find_all('li')
        rainfall_probability = int(lis[0].find('dd', class_='weather_item _dotWrapper').find('span').text) + int(lis[1].find('dd', class_='weather_item _dotWrapper').find('span').text) + int(lis[2].find('dd', class_='weather_item _dotWrapper').find('span').text) + int(lis[3].find('dd', class_='weather_item _dotWrapper').find('span').text) + int(lis[4].find('dd', class_='weather_item _dotWrapper').find('span').text)
        
        expected_rainfall = float(lis[0].find('dd', class_='item_condition').find('span').text) + float(lis[1].find('dd', class_='item_condition').find('span').text) + float(lis[2].find('dd', class_='item_condition').find('span').text)
        
        current_time = lis[0].find('dd', class_='item_time').find('span').text
        last_time = lis[4].find('dd', class_='item_time').find('span').text

        # 응답 설정
        answer = "< " + detail_location + " : " + date + "날씨 >\n"
        answer = answer + " - 현재온도 : " + current_temperature + "℃, 체감온도 : " + sensible_temperature + "℃\n - 최저온도 : " + min_temperature + "℃, 최고온도 : " + max_temperature + "℃\n\n"
        answer = answer + " - 미세먼지 : " + fine_dust + ", 초미세먼지 : " + ultra_fine_dust + "\n - 오존지수 : " + ozone_index + ", 자외선 : " + ultraviolet + "\n\n"
        answer = answer + " - 현재시간 : " + current_time + "\n - 강수확률 : " + str(rainfall_probability) + "%, 예상강수량 : " + str(expected_rainfall) + "mm\n\n"
        
        # 일교차, 우산관련 팁 응답
        if (int(max_temperature) - int(min_temperature) >= 0):
            diff = int(max_temperature) - int(min_temperature)
            answer = answer + "★일교차( " + str(diff) + "℃)가 심해요! 감기 조심하세요! :) ★\n"
        if expected_rainfall >= 0.0:
            answer = answer + "★비가 올 수도 있어요!(강수확률: " + str(expected_rainfall) + "%) 우산을 챙겨보아요 :) ★\n\n"  
        answer = answer + " # 강수확률은 " + current_time + "부터 " + last_time + " 까지의\n # 각 통계의 평균으로 나타낸 것입니다!ㅎ~ㅎ\n # 강수량은 " + current_time + "부터 " + last_time + " 까지의\n # 각 통계의 합으로 나타낸 것입니다!ㅎ-ㅎ"
        
    # 내일날씨
    elif date == "내일":
        answer = "< " + detail_location + " : " + date + "날씨 >\n"
        
        t = soup.find('div', class_='tomorrow_area _mainTabContent')
        t1 = t.find_all('div', class_='main_info morning_box')
        temperature = []
        
        # 오전오후 평균온도, 날씨, 미세먼지, 응답설정
        for div in t1:
            daytime = div.find('strong', class_='tlt').text
            avg_temperature = div.find('span', class_='todaytemp').text
            temperature.append(avg_temperature)
            
            t2 = div.find('div', class_='info_data').find('ul', class_='info_list')
            avg_weather = t2.find('p', class_='cast_txt').text
            fine_dust = t2.find('div', class_='detail_box').find('span', class_='indicator').span.text
            
            answer = answer + " * " + daytime + "\n - 날씨 : " + avg_weather + ", 평균기온 : " + avg_temperature + "℃\n"
            answer = answer + " - 미세먼지 : " + fine_dust + "\n\n"
        
        # 평균강수확률, 평균습도
        s = t.find('div', class_='table_info bytime _tomorrowWeatherByTime')
        
        s1 = s.find('div', class_='info_list rainfall _tabContent').find('ul', class_='list_area')
        lis1 = s1.find_all('li')
        avg_rainfall_probability = (int(lis1[3].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis1[4].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis1[5].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis1[6].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis1[7].find('dd', class_='weather_item _dotWrapper').span.text)) / 5
        
        s2 = s.find('div', class_='info_list humidity _tabContent').find('ul', class_='list_area')
        lis2 = s2.find_all('li')
        avg_humidity = (int(lis2[3].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis2[4].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis2[5].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis2[6].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis2[7].find('dd', class_='weather_item _dotWrapper').span.text)) / 5
        
        # 응답설정
        answer = answer + " - 강수확률 : " + str(avg_rainfall_probability) + "%\n - 예상습도 : " + str(avg_humidity) + "%\n\n"
        
        # 일교차, 강수확률 관련 응답
        if int(temperature[1]) - int(temperature[0]) >= 0:
            diff = int(temperature[1]) - int(temperature[0])
            answer = answer + "★일교차( " + str(diff) + "℃)가 심해요! 감기 조심하세요! :) ★\n"
        if avg_rainfall_probability >= 0:
            answer = answer + "★비가 올 수도 있어요!(강수확률: " + str(avg_rainfall_probability) + "%) 우산을 챙겨보아요 :) ★\n\n"
        
        answer = answer + " # 강수확률과 예상습도는 오전 9시부터 \n # 오후 9시까지의 각 통계의 평균으로\n # 나타낸 것입니다! ㅎ~ㅎ"
        
    # 모레날씨
    elif date == "모레":
        answer = "< " + detail_location + " : " + date + "날씨 >\n"
        t= soup.find('div', class_='tomorrow_area day_after _mainTabContent')
        t1 = t.find_all('div', class_='main_info morning_box')
        temperature = []
        
        # 오전오후 평균온도, 미세먼지, 날씨, 응답설정
        for div in t1:
            daytime = div.find('strong', class_='tlt').text
            avg_temperature = div.find('span', class_='todaytemp').text
            temperature.append(avg_temperature)
            
            t2 = div.find('div', class_='info_data').find('ul', class_='info_list')
            avg_weather = t2.find('p', class_='cast_txt').text
            fine_dust = t2.find('div', class_='detail_box').find('span', class_='indicator').span.text
            
            answer = answer + " * " + daytime + "\n - 날씨 : " + avg_weather + ", 평균기온 : " + avg_temperature + "℃\n"
            answer = answer + " - 미세먼지 : " + fine_dust + "\n\n"
            
        # 평균강수확률, 평균습도
        s = t.find('div', class_='table_info bytime _dayAfterWeatherByTime')
        s1 = s.find('div', class_='info_list rainfall _tabContent').find('ul', class_='list_area')
        lis1 = s1.find_all('li')
        avg_rainfall_probability = (int(lis1[3].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis1[4].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis1[5].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis1[6].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis1[7].find('dd', class_='weather_item _dotWrapper').span.text)) / 5
        
        s2 = s.find('div', class_='info_list humidity _tabContent').find('ul', class_='list_area')
        lis2 = s2.find_all('li')
        avg_humidity = (int(lis2[3].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis2[4].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis2[5].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis2[6].find('dd', class_='weather_item _dotWrapper').span.text) + int(lis2[7].find('dd', class_='weather_item _dotWrapper').span.text)) / 5
        
        # 응답 설정
        answer = answer + " - 강수확률 : " + str(avg_rainfall_probability) + "%\n - 예상습도 : " + str(avg_humidity) + "%\n\n"
        
        # 일교차, 강수확률 관련 응답
        if int(temperature[1]) - int(temperature[0]) >= 0:
            diff = int(temperature[1]) - int(temperature[0])
            answer = answer + "★일교차( " + str(diff) + "℃)가 심해요! 감기 조심하세요! :) ★\n"
        if avg_rainfall_probability >= 0:
            answer = answer + "★비가 올 수도 있어요!(강수확률: " + str(avg_rainfall_probability) + "%) 우산을 챙겨보아요 :) ★\n\n"
        
        answer = answer + " # 강수확률과 예상습도는 오전 9시부터 \n # 오후 9시까지의 각 통계의 평균으로\n # 나타낸 것입니다! ㅎ~ㅎ"
        

    return answer


# # 메인 함수
# if __name__ == '__main__':

#     app.run(host='0.0.0.0', port=5000, threaded=True)