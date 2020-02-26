import requests
from datetime import datetime
import pytz
import xmltodict
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
        for self.i in self._temp3:
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
        for i in self.temp_data['stations']:
            self.d_temp = data_temp()
            self.d_temp['Lat'] = i['lat']
            self.d_temp['Lng'] = i['long']
            # ToDo
            pass
    def check_datenow(self,time:str) -> bool:
        self.d = datetime.now(tz).strftime('%Y-%m-%d')
        return self.d in time
    def get_data(self):
        self._nrct()
        return self._data