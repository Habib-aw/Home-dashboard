

import requests
import json
from tkinter import Label
from PIL import ImageTk,Image
from datetime import datetime
import platform
import schedule
from Settings import frame3BgColor,dailyDayFontSize,dailyTempFontSize,dailyWeatherIconHeight,dailyWeatherIconWidth,hourlyWeatherDataFontSize,hourlyWeatherIconHeight,hourlyWeatherIconWidth,numOfWeatherHours,forecastsPaddingX,hourlyWeatherPaddingX,hourlyWeatherHeadingFontSize


def celsiusConvert(kelvin):
    return str(round(kelvin - 273.15))+"°C"
def getDay(i):
    daysOfWeek = ['Monday','Tuesday','Wednesday',
                        'Thursday','Friday','Saturday',"Sunday"]
    if i == 0:
        return "Today"
    dayWeekIndex = (datetime.now().weekday() + i) % 7
    return daysOfWeek[dayWeekIndex]

class Weather:
    def __init__(self,frame,errorMsgLabel):
        self.data = None
        self.errorMsgLabel = errorMsgLabel
        self.hourlyWeather = [["" for _ in range(numOfWeatherHours)] for _ in range(7)]
        self.hourlyWeatherLabels = [[None for _ in range(numOfWeatherHours)] for _ in range(7)]
        self.forecasts = [[None,None,None] for _ in range(7)]
        self.frame = frame
        self.getData()
        self.setHourlyWeather()
        self.setForecasts()
        self.showForecasts()
        self.showHourlyWeather()

        schedule.every(10).minutes.do(self.configHourlyWeather)
    def configHourlyWeather(self):
        self.getData()
        if self.data != "":
            self.setHourlyWeather()
            height = len(self.hourlyWeather[0])
            width = len(self.hourlyWeather)
            for i in range(height): 
                for j in range(width):
                    if j ==1 and i>0 :
                        img = ImageTk.PhotoImage(Image.open(self.hourlyWeather[j][i]).resize((hourlyWeatherIconWidth,hourlyWeatherIconHeight),Image.Resampling.LANCZOS))
                        self.hourlyWeatherLabels[j][i].config(image=img)
                        self.hourlyWeatherLabels[j][i].image = img
                    else:
                        self.hourlyWeatherLabels[j][i].config(text=self.hourlyWeather[j][i])
            self.setForecasts()
            self.showForecasts()
                
    def getData(self):
        try:
            res = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=51&lon=0&appid=0b0d6bb2481f89c3bbec13ddfa2879bd')
            self.data = json.loads(res.text)
            self.errorMsgLabel.pack_forget()
        except:
            self.data = ""
            self.errorMsgLabel.pack()
    def setHourlyWeather(self):
        for i in range(1,len(self.hourlyWeather[0])):
            hyphen = "-"
            if platform.system() =="Windows":
                hyphen="#"
            if self.data == "":
                self.hourlyWeather[0][i] = ''
                self.hourlyWeather[1][i] = ''
                self.hourlyWeather[2][i] = ''
                self.hourlyWeather[3][i] = ''
                self.hourlyWeather[4][i] = ''
                self.hourlyWeather[5][i] = ''
                self.hourlyWeather[6][i] = ''
            else:
                self.hourlyWeather[0][i] = datetime.utcfromtimestamp(self.data['hourly'][i]['dt']).strftime('%'+hyphen+'I%p')
                self.hourlyWeather[1][i] =  "Images/"+self.data['hourly'][i]['weather'][0]['icon']+".png"
                self.hourlyWeather[2][i] = celsiusConvert( self.data['hourly'][i]['temp'])
                self.hourlyWeather[3][i] = ""+celsiusConvert( self.data['hourly'][i]['feels_like'])
                self.hourlyWeather[4][i] = str(round(self.data['hourly'][i]['pop']*100))+"%"
                self.hourlyWeather[5][i] =  str(self.data['hourly'][i]['uvi'])
                self.hourlyWeather[6][i] =  str(round(self.data['hourly'][i]['wind_speed']* 2.236936))+" mph"

        self.hourlyWeather[2][0] = "Temperature"
        self.hourlyWeather[3][0] = "Feels like"
        self.hourlyWeather[4][0] = "Rain Chance"
        self.hourlyWeather[5][0] = "Uv index"
        self.hourlyWeather[6][0] = "Wind speed"

    def showHourlyWeather(self):
        height = len(self.hourlyWeather[0])
        width = len(self.hourlyWeather)
        for i in range(height): 
            for j in range(width):
                if i==0:
                    font = hourlyWeatherHeadingFontSize
                else:
                    font = hourlyWeatherDataFontSize
                if j ==1 and i>0 and self.data != "":
                    img = ImageTk.PhotoImage(Image.open(self.hourlyWeather[j][i]).resize((hourlyWeatherIconWidth,hourlyWeatherIconHeight),Image.Resampling.LANCZOS))
                    self.hourlyWeatherLabels[j][i] = Label(self.frame,image=img,background=frame3BgColor)
                    self.hourlyWeatherLabels[j][i].image = img
                else:
                    self.hourlyWeatherLabels[j][i] = Label(self.frame, text=self.hourlyWeather[j][i],background=frame3BgColor,font=("Arial",font),foreground="white")
                self.hourlyWeatherLabels[j][i].grid(row=i, column=j,ipadx=hourlyWeatherPaddingX)

    def setForecasts(self):
        for i in range(len(self.forecasts)):
            if self.data == "":
                self.forecasts[i] =[getDay(i),"",""]
            else:
                img = "Images/"+self.data['daily'][i]['weather'][0]['icon']+'.png'
                self.forecasts[i] = [getDay(i),img,celsiusConvert(self.data['daily'][i]['temp']['day'])]


    def showForecasts(self):
            height = 3
            width = len(self.forecasts)
            for i in range(height): 
                for j in range(width): 
                    fontSize = dailyTempFontSize
                    if i == 0:
                        fontSize = dailyDayFontSize
                    if i ==1 and self.data != "":
                        img =  ImageTk.PhotoImage(Image.open(self.forecasts[j][i]).resize((dailyWeatherIconWidth,dailyWeatherIconHeight),Image.Resampling.LANCZOS))
                        x = Label(self.frame,image=img,background=frame3BgColor)
                        x.image = img
                        
                    else:
                        x = Label(self.frame, text=self.forecasts[j][i],background=frame3BgColor,font=("Arial",fontSize),foreground="white")
                    x.grid(row=i+len(self.hourlyWeather[0]), column=j,ipadx=forecastsPaddingX)
