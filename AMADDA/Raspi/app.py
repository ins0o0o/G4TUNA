import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QPixmap
import openai
from ui_main import Ui_MainWindow
import resources_rc
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import urllib.request
import urllib.parse

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
openai.api_key = "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"

# calendar id
calendar_id_1 = 'cvbasd0920@naver.com'
calendar_id_2 = 'sohnjohn01@gmail.com'
calendar_id_3 = None
calendar_id_4 = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.profile4_button.setEnabled(False)
        self.ui.profile4_button.hide()
        self.ui.profile4_name.hide()
        # self.ui.profile3_button.setEnabled(False)
        # self.ui.profile3_button.hide()
        # self.ui.profile3_name.hide()
        # self.ui.profile2_button.setEnabled(False)
        # self.ui.profile2_button.hide()
        # self.ui.profile2_name.hide()

        # 2번째 일정 및 준비물
        self.ui.schedule_label_2_1.hide()
        self.ui.schedule_2.hide()
        self.ui.schedule_label_2_2.hide()
        self.ui.schedule_2_item.hide()
        # 3번째 일정 및 준비물
        self.ui.schedule_label_3_1.hide()
        self.ui.schedule_3.hide()
        self.ui.schedule_label_3_2.hide()
        self.ui.schedule_3_item.hide()

    def on_off_bt(self):
        a = 1

    def profile_bt1(self):
        self.weather_update()
        self.recommend_supplies(self.get_calendar_events(calendar_id_1))
    
    def profile_bt2(self):
        self.weather_update()
        self.recommend_supplies(self.get_calendar_events(calendar_id_2))

    def profile_bt3(self):
        self.weather_update()
        self.recommend_supplies(self.get_calendar_events(calendar_id_3))

    def profile_bt4(self):
        self.weather_update()
        self.recommend_supplies(self.get_calendar_events(calendar_id_4))
        
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
        events_title = list(events.keys())
        events_num = len(events_title)
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


app = QApplication(sys.argv)
window = MainWindow()
window.showFullScreen()
app.exec()
