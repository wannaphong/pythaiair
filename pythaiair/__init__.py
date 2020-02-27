import requests
from datetime import datetime
import pytz
import xmltodict
from tqdm import tqdm
import json

tz = pytz.timezone('Asia/Bangkok')
class Air(object):
    def __init__(self):
        self._data = []
    
    def data_temp(self):
        return {
            'Lat' : '',
            'Lng' : '',
            'aqi' : '',
            'pm2.5' : '',
            'pm10' : '',
            'CO' : '',
            'NO2' : '',
            'O3' : '',
            'SO2' : '',
            'title' : '',
            'time' : '',
            'source' : ''
        }
    def _nrct(self) -> None:
        self._url = "http://pm2_5.nrct.go.th/map"
        self._r = requests.get(self._url)
        self._html = self._r.text.strip('\n')
        self._temp2 = self._html.split(" var location")[1:]
        self._temp3 = []
        for self._i in self._temp2:
            self._temp3.append(self._i.split("google.maps.event.addListener(marker1aerosure, 'click', function() {")[0])
        for self.i in tqdm(self._temp3):
            self.d_temp = self.data_temp()
            self.temp1= self.i.split("new google.maps.LatLng(")
            self.LatLng = self.temp1[1].split(");")[0]
            self.d_temp['Lat'] = self.LatLng.split(",")[0]
            self.d_temp['Lng'] = self.LatLng.split(",")[1]
            self.temp1 = self.temp1[1]
            if "var aqi = '" in self.temp1:
                self.d_temp['aqi'] = self.temp1.split("var aqi = '")[1].split("'")[0]
            if 'var pm = "' in self.temp1:
                self.d_temp['pm2.5'] = self.temp1.split('var pm = "')[1].split('"')[0]
            self.d_temp['pm10'] = ''
            self.d_temp['CO'] = ''
            self.d_temp['NO2'] = ''
            self.d_temp['O3'] = ''
            self.d_temp['SO2'] = ''
            self.d_temp['title'] = self.temp1.split("data: '")[1].split("'")[0].strip()
            if "Air4Thai" in self.d_temp['title']:
                del self.d_temp
                continue
            self.d_temp['time'] = self.temp1.split("time: '")[1].split("'")[0]
            self.d_temp['source'] = "nrct"
            if self.check_datenow(self.d_temp['time']):
                self._data.append(self.d_temp)
    def _air4thai(self):
        self.url3 = "http://air4thai.pcd.go.th/services/getNewAQI_JSON.php"
        self.r3 = requests.get(self.url3)
        self.temp_data = dict(self.r3.json())
        for self.i in tqdm(self.temp_data['stations']):
            self.d_temp = self.data_temp()
            self.d_temp['Lat'] = self.i['lat']
            self.d_temp['Lng'] = self.i['long']
            self.l_temp = self.i['LastUpdate']
            self.d_temp['aqi'] = self.l_temp['AQI']['aqi']
            if 'PM25' in list(self.l_temp.keys()):
                self.pm25 = self.l_temp['PM25']['value']
                if self.pm25 != 'n/a' and self.pm25 != '' and self.pm25 != '-' and self.pm25 != 'N/A':
                    self.d_temp['pm2.5'] = self.pm25
            if 'PM10' in list(self.l_temp.keys()):
                self.pm10 = self.l_temp['PM10']['value']
                if self.pm10 != 'n/a' and self.pm10 != '' and self.pm10 != '-' and self.pm10 != 'N/A':
                    self.d_temp['pm10'] = self.pm10
            if 'CO' in list(self.l_temp.keys()):
                self.CO = self.l_temp['CO']['value']
                if self.CO != 'n/a' and self.CO != '' and self.CO != '-' and self.CO != 'N/A':
                    self.d_temp['CO'] = self.CO
            if 'NO2' in list(self.l_temp.keys()):
                self.NO2 = self.l_temp['NO2']['value']
                if self.NO2 != 'n/a' and self.NO2!='' and self.NO2 != '-' and self.NO2 != 'N/A':
                    self.d_temp['NO2'] = self.NO2
            if 'O3' in list(self.l_temp.keys()):
                self.O3 = self.l_temp['O3']['value']
                if self.O3 != 'n/a' and self.O3 != '' and self.O3 != '-' and self.O3 != 'N/A':
                    self.d_temp['O3'] = self.O3
            if 'SO2' in list(self.l_temp.keys()):
                self.SO2 = self.l_temp['SO2']['value']
                if self.SO2 != 'n/a' and self.SO2 != '' and self.SO2 != '-' and self.SO2 != 'N/A':
                    self.d_temp['SO2'] = self.SO2
            self.d_temp['title'] = self.i['areaTH']
            self.d_temp['time'] = self.l_temp['date'] + " " + self.l_temp['time']
            self.d_temp['source'] = "air4thai"
            if self.check_datenow(self.d_temp['time']):
                self._data.append(self.d_temp)
    def _bangkok(self):
        self.url2 = "https://bangkokairquality.com/bma/marker.php"
        self.r2 = requests.get(self.url2)
        self.data_bangkok = dict(json.loads(json.dumps(xmltodict.parse(self.r2.text),ensure_ascii=False)))
        for self.i in tqdm(self.data_bangkok['markers']['marker']):
            self.d_temp = self.data_temp()
            self.d_temp['Lat'] = self.i['@lat']
            self.d_temp['Lng'] = self.i['@lng']
            if '@pm25' in list(self.i.keys()):
                if self.i['@pm25'] != 'n/a' and self.i['@pm25'] != '' and self.i['@pm25'] != '-':
                    self.d_temp['pm2.5'] = self.i['@pm25']
            if '@pm10' in list(self.i.keys()):
                self.d_temp['pm10'] = self.i['@pm10']
            self.d_temp['title'] = self.i['@district_th'].strip() + " กรุงเทพฯ"
            self.d_temp['time'] = self.i['@date_time']
            self.d_temp['source'] = 'bangkokairquality'
            if self.check_datenow2(self.d_temp['time']):
                self.d = datetime.now(tz).strftime('%Y-%m-%d')
                self.d2 = datetime.now(tz).strftime('%d-%m-%Y')
                self.d_temp['time'] = self.d_temp['time'].replace(self.d2,self.d)
                self._data.append(self.d_temp)
    def check_datenow2(self,time:str) -> bool:
        self.d = datetime.now(tz).strftime('%d-%m-%Y')
        return self.d in time
    def check_datenow(self,time:str) -> bool:
        self.d = datetime.now(tz).strftime('%Y-%m-%d')
        return self.d in time
    def update_data(self):
        self._nrct()
        self._air4thai()
        self._bangkok()
    def get_data(self):
        return self._data