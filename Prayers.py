from Settings import frame1BgColor
from tkinter import Label
import json
from Settings import today,month,day,year,minsBeforeSalah,prayerFontSize,prayerLabelsPaddingX,otherPrayerLabelsPaddingX,adhaanCheckInterval,prayerPassedCheckInterval,mithlFontSize
from Jummah import firstJammah,secondJammah
from datetime import datetime,timedelta
from audioplayer import AudioPlayer
from threading import Thread
import schedule
import requests
from cec import *

def playNoise(soundFile,play=True):
    if play:
        switch_hdmi(2)
    AudioPlayer("Sounds/"+soundFile+".mp3").play(block=True)
class Prayers:
    # def __init__(self,frame):
    def __init__(self,frame,sehriText,sehriLabel,iftaarText,iftaarLabel):
        self.sehriText = sehriText
        self.sehriLabel = sehriLabel
        self.iftaarText = iftaarText
        self.iftaarLabel = iftaarLabel
        self.frame = frame
        self.prayerLength = 6
        self.schedulerSet = False
        self.mithl1TimeObj = None
        self.mithl1Label =None
        self.getPrayersScheduler=None
        self.prayerTimeObj = [[None for _ in range(2)] for _ in range (5)]
        self.prayerLabels = [[None for _ in range(2)] for _ in range (5)]
        self.getPrayers()
        self.adhaanAnnounce = False
        self.startAnnounceIndex= 0
        self.salahAnnounceIndex = 0
        self.salahAnnounce = False
        schedule.every(adhaanCheckInterval).seconds.do(self.announceAdhaanAndSalah)
    def salahsToDate(self):
        if self.prayers [1][1] != "":
            for i in range(1,self.prayerLength):
                for j in range(1,len(self.prayers[0])):
                    salahsSplit = self.prayers[i][j].split(":")
                    if i == 1 or (i ==2 and (salahsSplit[0]=="12" or salahsSplit[0]=="11")):
                        self.prayerTimeObj[i-1][j-1] = datetime(year,month+1,day+1,int(salahsSplit[0]),int(salahsSplit[1]))
                    else:
                        self.prayerTimeObj[i-1][j-1] = datetime(year,month+1,day+1,int(salahsSplit[0])+12,int(salahsSplit[1]))
            salahsSplit = self.mithl1Time.split(":")
            self.mithl1TimeObj = datetime(year,month+1,day+1,int(salahsSplit[0])+12,int(salahsSplit[1]))
    def getPrayers(self):
        try:
            # res = requests.get('https://data.baitulmamur.academy/')
            # self.data = json.loads(res.text)
            self.data = json.load(open(str(today.year)+".json"))
            self.prayers = [
                ["","Start","Jama'ah"],
                ["Fajr",self.data[month][day]['Fajr_start'],self.data[month][day]['Fajr_jamaah']],
                ["Zuhr",self.data[month][day]['Zuhr_start'],self.data[month][day]['Zuhr_jamaah']],
                ["Asr",self.data[month][day]['Asr_start2'],self.data[month][day]['Asr_jamaah']],
                ["Maghrib",self.data[month][day]['Maghrib_start'],self.data[month][day]['Maghrib_jamaah']],
                ["Isha",self.data[month][day]['Isha_start'],self.data[month][day]['Isha_jamaah']],
                ["Sunrise",self.data[month][day]['Sunrise'],"-"],
                ["","First","Second"],
                ["Jummah",firstJammah,secondJammah]
            ]
            self.mithl1Time = self.data[month][day]['Asr_start1']
            self.salahsToDate()
            schedule.cancel_job(self.getPrayersScheduler)
            self.schedulerSet = False
        except Exception as e:
            print("Error!",e)
            self.prayers = [
                ["","Start","Jama'ah"],
                ["Fajr","",""],
                ["Zuhr","",""],
                ["Asr","",""],
                ["Maghrib","",""],
                ["Isha","",""],
                ["Sunrise","","-"],
                ["","First","Second"],
                ["Jummah",firstJammah,secondJammah]
            ]
            self.mithl1Time = ""
            if not self.schedulerSet:
                self.schedulerSet=True
                self.getPrayersScheduler = schedule.every(2).minutes.do(self.getPrayers)
        self.showPrayers()
    def showPrayers(self):
        height = len(self.prayers)
        width = len(self.prayers[0])

        for i in range(height): 
            for j in range(width):
                if i >3:
                    addRow = 1
                else: 
                    addRow = 0
                if j == 0:
                    addColumn = 0
                    columnspan = 2
                else:
                    columnspan=1
                    addColumn = 1
                if i == 3:
                    if j == 0:
                        self.prayerLabels[i-1][j-1]= Label(self.frame, text=self.prayers[i][j],background=frame1BgColor,font=("Arial",prayerFontSize),foreground="white")
                        self.prayerLabels[i-1][j-1].grid(row=i+addRow, column=j+addColumn,ipadx=prayerLabelsPaddingX,rowspan=2)
                        mithl1= Label(self.frame, text="Mithl 1",background=frame1BgColor,font=("Arial",mithlFontSize),foreground="white")
                        mithl1.grid(row=i+addRow, column=j+1,ipadx=prayerLabelsPaddingX)
                        mithl2= Label(self.frame, text="Mithl 2",background=frame1BgColor,font=("Arial",mithlFontSize),foreground="white")
                        mithl2.grid(row=i+1, column=j+1,ipadx=prayerLabelsPaddingX)
                    elif j==1:
                        self.mithl1Label= Label(self.frame, text=self.mithl1Time,background=frame1BgColor,font=("Arial",prayerFontSize),foreground="white")
                        self.mithl1Label.grid(row=i+addRow, column=j+addColumn,ipadx=prayerLabelsPaddingX)
                        self.prayerLabels[i-1][j-1]= Label(self.frame, text=self.prayers[i][j],background=frame1BgColor,font=("Arial",prayerFontSize),foreground="white")
                        self.prayerLabels[i-1][j-1].grid(row=i+1, column=j+addColumn,ipadx=prayerLabelsPaddingX)
                    elif j ==2:
                        self.prayerLabels[i-1][j-1]= Label(self.frame, text=self.prayers[i][j],background=frame1BgColor,font=("Arial",prayerFontSize),foreground="white")
                        self.prayerLabels[i-1][j-1].grid(row=i+addRow, column=j+addColumn,ipadx=prayerLabelsPaddingX,rowspan=2)
                        
                elif(i>0 and i<(self.prayerLength)) and j!=0:
                    self.prayerLabels[i-1][j-1]= Label(self.frame, text=self.prayers[i][j],background=frame1BgColor,font=("Arial",prayerFontSize),foreground="white")
                    self.prayerLabels[i-1][j-1].grid(row=i+addRow, column=j+addColumn,ipadx=prayerLabelsPaddingX,columnspan=columnspan)
                else:
                    notPrayer =Label(self.frame, text=self.prayers[i][j],background=frame1BgColor,font=("Arial",prayerFontSize),foreground="white")
                    notPrayer.grid(row=i+addRow, column=j+addColumn,ipadx=otherPrayerLabelsPaddingX,columnspan=columnspan)
        if self.prayers [1][1] != "":
            self.checkPrayerPassed()

    def checkPrayerPassed(self):
        if self.prayers [1][1] != "":
            setJamaah = False
            for i in range(len(self.prayerTimeObj)):
                if (self.prayerTimeObj[i][0]<datetime.now()):
                    self.prayerLabels[i][0].config(background="green")
                    if i == 0:
                        self.sehriLabel.config(text=self.sehriText)
                    if i == 3:
                        self.iftaarLabel.config(text=self.iftaarText)
                if (self.prayerTimeObj[i][1]<=datetime.now()):
                    self.prayerLabels[i][1].config(background="red")
                if datetime.now()<=self.prayerTimeObj[i][1] and not setJamaah:
                    self.prayerLabels[i][1].config(background="orange")
                    setJamaah=True
            for i in range(len(self.prayerTimeObj)):
                if i == len(self.prayerTimeObj)-1:
                    break
                if(self.prayerTimeObj[i+1][0]<datetime.now()):
                    self.prayerLabels[i][0].config(background="red")
            if datetime.now() >= self.mithl1TimeObj:
                self.mithl1Label.config(background="green")
            if datetime.now() >= self.prayerTimeObj[3][0]:
                self.mithl1Label.config(background="red")
    def announceAdhaanAndSalah(self):
        if self.prayers [1][1] != "":
            for i in range(len(self.prayerTimeObj)):
                if(datetime.now() >= self.prayerTimeObj[i][0] and datetime.now() <(self.prayerTimeObj[i][0]+timedelta(minutes=1))) and not self.adhaanAnnounce:
                    self.adhaanAnnounce = True
                    self.startAnnounceIndex = i
                    self.checkPrayerPassed()
                    if i ==0:
                        Thread(target=playNoise,args=("adhaan-new",)).start()
                    else:
                        Thread(target=playNoise,args=("adhaan-new-long",)).start()
                    break
                if(datetime.now() >= (self.prayerTimeObj[i][1] - timedelta(minutes=minsBeforeSalah)) and datetime.now() <(self.prayerTimeObj[i][1]-timedelta(minutes=(minsBeforeSalah-1))) and not self.salahAnnounce):
                    self.salahAnnounce = True
                    self.salahAnnounceIndex = i
                    Thread(target=playNoise,args=("salah",False,)).start()
                    break
                if(datetime.now() >= (self.prayerTimeObj[i][1]) and datetime.now() <(self.prayerTimeObj[i][1]+timedelta(minutes=1))):
                    self.checkPrayerPassed()
            if not (datetime.now() >= self.prayerTimeObj[self.startAnnounceIndex][0] and datetime.now() <(self.prayerTimeObj[self.startAnnounceIndex][0]+timedelta(minutes=1))):
                self.adhaanAnnounce = False
            if not (datetime.now() >= (self.prayerTimeObj[self.salahAnnounceIndex][1] - timedelta(minutes=minsBeforeSalah)) and datetime.now() <(self.prayerTimeObj[self.salahAnnounceIndex][1]-timedelta(minutes=(minsBeforeSalah-1)))):
                self.salahAnnounce = False