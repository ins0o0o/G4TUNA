import sys
import threading
from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, QThread, Signal
import openai
from ui_main import Ui_MainWindow
from ui_second import Ui_MainWindow as Ui_SecondWindow  
import resources_rc
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import urllib.request
import urllib.parse
from time import sleep

# 오늘 날짜를 자동으로 가져와 필요한 형식으로 사용
today_date = datetime.today().strftime('%Y%m%d')  # YYYYMMDD 형식
today_date_hyphen = datetime.today().strftime('%Y-%m-%d')  # YYYY-MM-DD 형식

# base time 찾기
def get_base_time():
    current_time = datetime.now() - timedelta(hours=1)  # 현재 시각에서 1시간 빼기
    hour = current_time.hour

    # 예보 가능한 기준 시간대 설정
    forecast_times = [2, 5, 8, 11, 14, 17, 20, 23]
    
    # 가장 가까운 예보 기준 시간 찾기
    base_hour = max([t for t in forecast_times if t <= hour], default=2)
    
    # 예보 기준 시간 포맷팅
    return f"{base_hour:02}00"

# Google calendar API Key
google_key = "AIzaSyA2KUAo4fugxxjo4zG2iHMy1FS70zbls8A"

# openAI chatGPT API Key
openai.api_key = ""

# User Class
user_data_list = []

user_flag = -1

class SensorThread(QThread):
    sensor_detected = Signal()  # 센서가 감지되었을 때 신호 발생
    PIR_PIN = 17
    GPIO.setmode(GPIO.BCM)      # GPIO 초기화
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)

    def run(self):
        import time
        while True:
            if GPIO.input(self.PIR_PIN):
                self.sensor_detected.emit()  # 메인 쓰레드에 신호 보냄
            time.sleep(0.1)  # 100ms 주기로 센서 확인

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.timer = QTimer(self)
        self.timer.setInterval(5000)  # 5분
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.start()

        self.timer2 = QTimer(self)
        self.timer2.setInterval(500)  # 0.5초
        self.timer2.timeout.connect(self.update_profiles)
        self.timer2.start()

        self.sensor_thread = SensorThread()
        self.sensor_thread.sensor_detected.connect(self.PIR_detect)
        self.sensor_thread.start()


        # 2번째 리스트 감추기
        self.ui.schedule_label_2_1.hide()
        self.ui.schedule_2.hide()
        self.ui.schedule_label_2_2.hide()
        self.ui.schedule_2_item.hide()
        # 3번째 리스트 감추기
        self.ui.schedule_label_3_1.hide()
        self.ui.schedule_3.hide()
        self.ui.schedule_label_3_2.hide()
        self.ui.schedule_3_item.hide()

        # 프로필 감추기
        self.ui.profile4_button.setEnabled(False)
        self.ui.profile4_button.hide()
        self.ui.profile4_name.hide()
        self.ui.profile3_button.setEnabled(False)
        self.ui.profile3_button.hide()
        self.ui.profile3_name.hide()
        self.ui.profile2_button.setEnabled(False)
        self.ui.profile2_button.hide()
        self.ui.profile2_name.hide()
        self.ui.profile1_button.setEnabled(False)
        self.ui.profile1_button.hide()
        self.ui.profile1_name.hide()

        self.second_window = SecondWindow(self)

    def update_profiles(self):
        # user_data_list의 요소 개수를 가져옴
        user_count = len(user_data_list)

        # 최대 4개의 프로필 버튼을 활성화/비활성화
        profiles = [
            (self.ui.profile1_button, self.ui.profile1_name),
            (self.ui.profile2_button, self.ui.profile2_name),
            (self.ui.profile3_button, self.ui.profile3_name),
            (self.ui.profile4_button, self.ui.profile4_name),
        ]

        for i, (button, name) in enumerate(profiles):
            if i < user_count:
                # 활성화
                button.setEnabled(True)
                button.show()
                name.show()
                name.setText(user_data_list[i].user_name)  # 해당 유저 이름 설정
            else:
                # 비활성화
                button.setEnabled(False)
                button.hide()
                name.hide()

        if user_flag == 0 :
            self.ui.custom_item.setText(self.makeDayItem(user_data_list[0]))
        elif user_flag == 1:
            self.ui.custom_item.setText(self.makeDayItem(user_data_list[1]))
        elif user_flag == 2:
            self.ui.custom_item.setText(self.makeDayItem(user_data_list[2]))
        elif user_flag == 3:
            self.ui.custom_item.setText(self.makeDayItem(user_data_list[3]))


    def PIR_detect(self):
        if self.second_window.isHidden() is False:
            self.second_window.hide()
            GPIO.output(27,GPIO.HIGH)
            sleep(1000)
            GPIO.output(27,GPIO.LOW)
        self.timer.start()
    
    def on_timer_timeout(self):
        self.second_window = SecondWindow(self)
        self.second_window.showFullScreen()

    def on_off_bt(self):
        if self.ui.OnOff_button.isChecked():
            self.timer2.start()
        else:
            self.timer2.stop()

    def profile_bt1(self):
        self.weather_update()
        self.recommend_supplies(self.get_calendar_events(user_data_list[0].user_email))
        self.ui.custom_item.setText(self.makeDayItem(user_data_list[0]))
        global user_flag 
        user_flag = 0
    
    def profile_bt2(self):
        self.weather_update()
        self.recommend_supplies(self.get_calendar_events(user_data_list[1].user_email))
        self.ui.custom_item.setText(self.makeDayItem(user_data_list[1]))
        global user_flag 
        user_flag = 1

    def profile_bt3(self):
        self.weather_update()
        self.recommend_supplies(self.get_calendar_events(user_data_list[2].user_email))
        self.ui.custom_item.setText(self.makeDayItem(user_data_list[2]))
        global user_flag 
        user_flag = 2

    def profile_bt4(self):
        self.weather_update()
        self.recommend_supplies(self.get_calendar_events(user_data_list[3].user_email))
        self.ui.custom_item.setText(self.makeDayItem(user_data_list[3]))
        global user_flag 
        user_flag = 3

    from datetime import datetime

    def makeDayItem(self, user_data):
        # 오늘의 요일을 가져옴 (0: 월, 1: 화, ..., 6: 일)
        day_names = ['월', '화', '수', '목', '금', '토', '일']
        today_index = datetime.today().weekday()
        today_name = day_names[today_index]

        # user_data.schedule에서 오늘의 요일에 해당하는 아이템 추출
        today_items = user_data.schedule.get(today_name, [])

        # 아이템을 문자열로 변환 (콤마로 구분)
        return ', '.join(today_items) if today_items else "오늘은 준비물이 없습니다."
    

    # 날씨 정보 업데이트
    def weather_update(self):
        w_item_temp = 0
        weather_item_text = ''
        if self.get_weather_forecast() >= 45:
            weather_item_text += '우산'
            w_item_temp = 1
        if self.get_uv_index() != '낮음':
            if w_item_temp == 1:
                weather_item_text += '\n\n'
            weather_item_text += '선크림'
            w_item_temp = 1
        if self.get_dust_forecast() not in ['보통','좋음']:
            if w_item_temp == 1:
                weather_item_text += '\n\n'
            weather_item_text += '마스크'
        self.ui.weather_item.setText(weather_item_text)
        
    # 하늘상태, 온도, 습도, 강수확률 API
    def get_weather_forecast(self):
        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        params = {
            'serviceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
            'pageNo': '1',
            'numOfRows': '1000',
            'dataType': 'XML',
            'base_date': today_date,
            'base_time': '0500',  # 현재 시간에서 1시간 뺀 값을 사용
            'nx': '61',
            'ny': '126'
        }
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("기상 예보 요청 실패:", response.status_code)
            self.ui.rain_probability.setText("강수확률 ??%")
            return

        root = ET.fromstring(response.content)
        temperature = None
        humidity = None
        precipitation_probability = None
        sky_status = None
        rain_status = None

        for item in root.iter('item'):
            category = item.find('category').text
            obsr_value = item.find('fcstValue').text

            if category == 'TMP':  # TMP: 1시간 기온
                temperature = obsr_value
            elif category == 'REH':  # REH: 습도
                humidity = obsr_value
            elif category == 'POP':  # POP: 강수확률
                precipitation_probability = int(obsr_value)
            elif category == 'SKY':  # SKY: 하늘 상태
                sky_status = obsr_value
            elif category == 'PTY':  # PTY: 강수 형태
                rain_status = obsr_value

        if temperature is not None and humidity is not None:
            self.ui.temp_humid.setText(f"온도:{temperature}°C  습도:{humidity}%")
        else:
            self.ui.temp_humid.setText("온도: ??°C  습도: ??%")
            print("날씨 정보를 찾을 수 없습니다.")

        if precipitation_probability is not None:
            self.ui.rain_probability.setText(f"강수확률 {precipitation_probability}%")
        else:
            self.ui.rain_probability.setText("강수확률 ??%")
            print("강수확률 정보를 찾을 수 없습니다.")

        if sky_status is not None and rain_status is not None:
            if rain_status == '0': # 없음
                if sky_status in ['0','1','2','3']:
                    self.ui.weather_image.setPixmap(QPixmap(":/weather/free-icon-sun-1163764.png"))   # 맑은 하늘
                elif sky_status in ['4','5','6']:
                    self.ui.weather_image.setPixmap(QPixmap(":/weather/free-icon-cloudy-1163763.png"))   # 해, 구름
                elif sky_status in ['7','8']:
                    self.ui.weather_image.setPixmap(QPixmap(":/weather/free-icon-cloud-1163726.png"))   # 구름
                elif int(sky_status)>=9:
                    self.ui.weather_image.setPixmap(QPixmap(":/weather/free-icon-cloudy-1163736.png"))   # 흐림
            if rain_status == '1' or rain_status =='4': # 비, 소나기
                self.ui.weather_image.setPixmap(QPixmap(":/weather/free-icon-rainy-1163728.png"))   # 비
            if rain_status == '2' or rain_status =='3': # 눈
                self.ui.weather_image.setPixmap(QPixmap(":/weather/free-icon-snowy-1163731.png"))   # 눈
        else:
            self.ui.weather_image.setPixmap(QPixmap(":/title/free-icon-tuna-605314.png"))
            print("하늘 상태 정보를 찾을 수 없습니다.")

        if precipitation_probability is None:
            return 0
        return precipitation_probability
    

    # 자외선 수치 API
    def get_uv_index(self):
        url = 'http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4'
        queryParams = '?' + urllib.parse.urlencode({
            urllib.parse.quote_plus('ServiceKey'): 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
            urllib.parse.quote_plus('areaNo'): '1121571000',
            urllib.parse.quote_plus('time'): today_date + '14',
            urllib.parse.quote_plus('dataType'): 'XML'
        })

        request = urllib.request.Request(url + queryParams)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            root = ET.fromstring(response_body)
            
            uv_index = root.find('.//h3')
            if uv_index is not None:
                uv_value = int(uv_index.text)
                if uv_value >= 0 and uv_value <3:
                    uv_level = '낮음'
                elif uv_value >= 3 and uv_value <6:
                    uv_level = '보통'
                elif uv_value >= 6:
                    uv_level = '높음'
            else:
                uv_level = '??'

            self.ui.uv_level.setText(f"자외선 지수 {uv_value}({uv_level})")
            return uv_level


    # 미세먼지 등급 API
    def get_dust_forecast(self):
        url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'
        params = {
            'serviceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
            'returnType': 'xml',
            'numOfRows': '1',
            'pageNo': '1',
            'searchDate': today_date_hyphen,
            'InformCode': 'PM10'
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("미세먼지 예보 요청 실패:", response.status_code)
            return

        root = ET.fromstring(response.content)
        
        for item in root.iter('item'):
            inform_data = item.find('informData').text
            inform_grade = item.find('informGrade').text
            
            if inform_data == today_date_hyphen:
                grade_info = [info.strip() for info in inform_grade.split(',') if '서울' in info]
                seoul_grade = grade_info[0] if grade_info else "정보 없음"
                dust_level = seoul_grade.split(' : ')[1]
                self.ui.dust_level.setText(f"미세먼지 {dust_level}")
                return dust_level
            

    # Google Calendar API
    def get_calendar_events(self,calendar_id):
        today = datetime.utcnow().date()
        start_time = f"{today}T00:00:00Z"
        end_time = f"{today}T23:59:59Z"

        url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
        params = {
            "key": google_key,
            "timeMin": start_time,
            "timeMax": end_time,
            "singleEvents": "true",
            "orderBy": "startTime"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            events = response.json().get("items", [])
            event_dic = {}
            if not events:
                print("오늘 일정은 없습니다.")
            else:
                for event in events:
                    title = event.get("summary", "제목 없음")
                    start_time = event.get("start", {}).get("dateTime", "").split("T")[1][:5]
                    event_dic[title]=start_time
                return event_dic
        else:
            print("Error:", response.status_code, response.text)


    # 일정 제목에 따라 준비물 추천 함수
    def recommend_supplies(self,events):
        
        if events is None:
            events_title = []
            events_num = 0
        else:
            events_title = list(events.keys())
            events_num = len(events)
            

        item_recommanded = ['제발','되라','시발']
        # 추천 아이템 생성
        for i in range(events_num):
            prompt = f"'{events_title[i]}'라는 일정 제목 맞춰 챙겨 해당 일정에 필요한 챙겨나갈 준비물 세 가지를 추천해줘. 설명은 필요 없고  형식은 무조건 \n\n로 구분된 세단어로 답변해.예를 들면 '우산\n\n선크림\n\n마스크'와 같이 말이야."
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=50,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                # ChatGPT의 응답에서 준비물 추천 내용을 출력
                supplies = response.choices[0].message['content'].strip()
                print(supplies)
                item_recommanded[i]=supplies
            except Exception as e:
                print("준비물 추천 오류:", e)

        # 일정 UI 수정
        if events_num == 0:
            # 스케줄 컨텐츠 작성
            self.ui.schedule_1.setText('오늘 일정이 없습니다.')
            self.ui.schedule_1_item.setText('')
            # 2번째 리스트 감추기
            self.ui.schedule_label_2_1.hide()
            self.ui.schedule_2.hide()
            self.ui.schedule_label_2_2.hide()
            self.ui.schedule_2_item.hide()
            # 3번째 리스트 감추기
            self.ui.schedule_label_3_1.hide()
            self.ui.schedule_3.hide()
            self.ui.schedule_label_3_2.hide()
            self.ui.schedule_3_item.hide()
        elif events_num == 1:
            # 스케줄 컨텐츠 작성
            self.ui.schedule_1.setText(f'{events_title[0]}\n{events[events_title[0]]}')
            self.ui.schedule_1_item.setText(item_recommanded[0])
            # 2번째 리스트 감추기
            self.ui.schedule_label_2_1.hide()
            self.ui.schedule_2.hide()
            self.ui.schedule_label_2_2.hide()
            self.ui.schedule_2_item.hide()
            # 3번째 리스트 감추기
            self.ui.schedule_label_3_1.hide()
            self.ui.schedule_3.hide()
            self.ui.schedule_label_3_2.hide()
            self.ui.schedule_3_item.hide()
        elif events_num == 2:
            # 2번째 리스트 생성
            self.ui.schedule_label_2_1.show()
            self.ui.schedule_2.show()
            self.ui.schedule_label_2_2.show()
            self.ui.schedule_2_item.show()
            # 스케줄 컨텐츠 작성
            self.ui.schedule_1.setText(f'{events_title[0]}\n{events[events_title[0]]}')
            self.ui.schedule_1_item.setText(item_recommanded[0])
            self.ui.schedule_2.setText(f'{events_title[1]}\n{events[events_title[1]]}')
            self.ui.schedule_2_item.setText(item_recommanded[1])
             # 3번째 리스트 감추기
            self.ui.schedule_label_3_1.hide()
            self.ui.schedule_3.hide()
            self.ui.schedule_label_3_2.hide()
            self.ui.schedule_3_item.hide()
        elif events_num == 3:
            # 2번째 리스트 생성
            self.ui.schedule_label_2_1.show()
            self.ui.schedule_2.show()
            self.ui.schedule_label_2_2.show()
            self.ui.schedule_2_item.show()
            # 3번째 리스트 생성
            self.ui.schedule_label_3_1.show()
            self.ui.schedule_3.show()
            self.ui.schedule_label_3_2.show()
            self.ui.schedule_3_item.show()
            # 스케줄 컨텐츠 작성
            self.ui.schedule_1.setText(f'{events_title[0]}\n{events[events_title[0]]}')
            self.ui.schedule_1_item.setText(item_recommanded[0])
            self.ui.schedule_2.setText(f'{events_title[1]}\n{events[events_title[1]]}')
            self.ui.schedule_2_item.setText(item_recommanded[1])
            self.ui.schedule_3.setText(f'{events_title[2]}\n{events[events_title[2]]}')
            self.ui.schedule_3_item.setText(item_recommanded[2])

class SecondWindow(QMainWindow):
    def __init__(self,main_window):
        super().__init__()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.main_window.timer.stop()
        self.main_window.timer2.stop()


    def back2main(self):
        self.hide()
        self.main_window.timer.start()
        self.main_window.timer2.start()


flask_app = Flask(__name__)

@flask_app.route('/receive-data', methods=['POST'])
def update_data():
    data = request.json  # JSON 데이터 수신
    global user_flag 
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # 삭제 요청 처리
    if data.get('delete', False):
        user_flag = -1
        email_to_delete = data.get('email')
        if not email_to_delete:
            return jsonify({"error": "No email provided for deletion"}), 400
        
        # user_data_list에서 해당 email을 가진 클래스 삭제
        for index, user in enumerate(user_data_list):
            if user.user_email == email_to_delete:
                del user_data_list[index]
                print(f"User {email_to_delete} 데이터 삭제")
                return jsonify({"status": "success", "message": f"User {email_to_delete} deleted"}), 200

        print(f"User {email_to_delete}를 찾을 수 없음")
        return jsonify({"error": f"User {email_to_delete} not found"}), 404

    # 새 사용자 데이터 처리
    new_user = process_user_data(data)
    
    # user_data_list에서 user_email 검사
    for index, user in enumerate(user_data_list):
        if user.user_email == new_user.user_email:
            # 동일한 user_email이 있다면 기존 인스턴스를 덮어쓰기
            user_data_list[index] = new_user
            print(f"User {new_user.user_email} 데이터 갱신")
            user_flag = index
            return jsonify({"status": "success", "message": f"User {new_user.user_email} updated"}), 200

    # user_email이 없다면 배열에 새 인스턴스를 추가
    user_data_list.append(new_user)
    user_flag = len(user_data_list)-1
    print(f"User {new_user.user_email} 데이터 추가")
    
    return jsonify({"status": "success", "message": f"User {new_user.user_email} added"}), 200

def run_flask():
    flask_app.run(host="0.0.0.0", port=5000, debug = False)

class UserData:
    def __init__(self, user_email, user_name):
        self.user_email = user_email  # 사용자 이메일
        self.user_name = user_name  # 사용자 이름
        # 월, 화, 수, 목, 금, 토, 일 키를 가지는 딕셔너리
        self.schedule = {day: [] for day in ['월', '화', '수', '목', '금', '토', '일']}

    def add_item(self, item, repeat):
        # `repeat` 문자열을 분석하여 해당 요일에 아이템 추가
        if '주중' in repeat:
            for day in ['월', '화', '수', '목', '금']:
                self.schedule[day].append(item)
        elif '주말' in repeat:
            for day in ['토', '일']:
                self.schedule[day].append(item)
        elif '매일' in repeat:
            for day in self.schedule.keys():
                self.schedule[day].append(item)
        else:
            # 특정 요일에만 반복
            for day in repeat.split(', '):
                if day in self.schedule:
                    self.schedule[day].append(item)

def process_user_data(data):
    user_email = data.get('userEmail')
    user_name = data.get('userName')
    user = UserData(user_email, user_name)  # 사용자 클래스 생성

    # `item_n`과 `repeat_n` 처리
    for key, value in data.items():
        if key.startswith('item_'):
            index = key.split('_')[1]  # `n` 값 추출
            repeat_key = f'repeat_{index}'  # 매칭되는 repeat 키 생성
            repeat_value = data.get(repeat_key, '')  # repeat 값 가져오기
            user.add_item(value, repeat_value)  # 아이템과 반복 정보 추가
    return user


flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

app = QApplication(sys.argv)
window = MainWindow()
window.showFullScreen()

sys.exit(app.exec())
