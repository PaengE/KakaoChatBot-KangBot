from flask import Flask, request, jsonify
import where_is_bus as wib
import station_status as ss
import menu_dormitory_cafeteria as mdc
import menu_school_cafeteria as msc
import weather as wt

app = Flask(__name__)

# app.route는 flask의 기능으로, '/whereisbus'와 같은 url로 요청이 들어오면 해당 함수만 호출한다.
@app.route('/whereisbus', methods=['POST'])
def WhereIsBus():

    # 카카오톡 서버에서 json 형식의 메시지 받기
    req = request.get_json()
    # 메시지에서 데이터 받기
    bus_num = req["action"]["detailParams"]["bus_num"]["value"]
    
    # answer에 보낼 메시지 할당
    answer = "<< " + bus_num + "번 버스 실시간 위치 정보입니다. >>\n" + wib.search_bus(bus_num)

    
    # 보낼 데이터를 json으로 변환하여 전송
    return json_ify(answer)

@app.route('/stationstatus', methods=['POST'])
def StationStatus():

    
    req = request.get_json()
    
    station_name = req["action"]["detailParams"]["station_name"]["value"]
    
    answer = "<< " +  station_name + "정류장 실시간 접근 버스 정보입니다. >> \n" + ss.search_station(station_name)
    
    return json_ify(answer)

@app.route('/menu_dormitory_cafeteria', methods=['POST'])
def MenuDormitoryCafeteria():
    
    req = request.get_json()
    
    cafeteria = req["action"]["detailParams"]["cafeteria_2"]["value"]
    date = req["action"]["detailParams"]["sys_date"]["origin"]
    mealtime = req["action"]["detailParams"]["mealtime"]["value"]
    
    return json_ify(mdc.menu_dormitory_cafeteria(cafeteria,date,mealtime))

@app.route('/weather', methods=['POST'])
def Weather():
    
    req = request.get_json()

    location = req["action"]["detailParams"]["sys_location"]["value"]
    date = req["action"]["detailParams"]["sys_date"]["origin"]
    
    return json_ify(wt.weather(location,date))
   
@app.route('/menu_school_cafeteria', methods=['POST'])
def MenuSchoolCafeteria():
    
    req = request.get_json()
    
    cafeteria = req["action"]["detailParams"]["cafeteria_1"]["value"]
    date = req["action"]["detailParams"]["sys_date"]["origin"]
    # menu_type = req["action"]["detailParams"]["menu_type"]["value"]
    mealtime = req["action"]["detailParams"]["mealtime"]["value"]
    
    return json_ify(msc.menu_school_cafeteria(cafeteria,date,mealtime))
    

def json_ify(response):
    # 카카오톡 서버로 보낼 메시지
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText":{
                        "text":response
                    }
                }
            ]
        }
    }
    return res

# 메인 함수
if __name__ == '__main__':

    app.run(host='0.0.0.0', threaded=True)