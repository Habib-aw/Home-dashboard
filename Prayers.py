from Settings import frame1BgColor
from tkinter import Label
import json
from Settings import today,month,day,year,minsBeforeSalah,prayerFontSize,prayerLabelsPaddingX,otherPrayerLabelsPaddingX,adhaanCheckInterval,prayerPassedCheckInterval
from Jummah import firstJammah,secondJammah
from datetime import datetime,timedelta
from audioplayer import AudioPlayer
from threading import Thread
import schedule

def playNoise(soundFile):
    AudioPlayer("Sounds/"+soundFile+".mp3").play(block=True)
class Prayers:
    def __init__(self,frame):
        self.frame = frame
        self.data = json.load(open(str(today.year)+".json"))
        self.prayers = [
            ["","Start","Jama'ah"],
            ["Fajr",self.data[month][day]['Fajr_start'],self.data[month][day]['Fajr_jamaah']],
            ["Zuhr",self.data[month][day]['Zuhr_start'],self.data[month][day]['Zuhr_jamaah']],
            ["Asr",self.data[month][day]['Asr_start1'],self.data[month][day]['Asr_jamaah']],
            ["Maghrib",self.data[month][day]['Maghrib_start'],self.data[month][day]['Maghrib_jamaah']],
            ["Isha",self.data[month][day]['Isha_start'],self.data[month][day]['Isha_jamaah']],
            ["","First","Second"],
            ["Jummah",firstJammah,secondJammah]
        ]
        self.prayerTimeObj = [[None for _ in range(2)] for _ in range (5)]
        self.prayerLabels = [[None for _ in range(2)] for _ in range (5)]
        self.salahsToDate()
        self.showPrayers()
        self.checkPrayerPassed()
        self.adhaanAnnounce = False
        self.startAnnounceIndex= 0
        self.salahAnnounceIndex = 0
        self.salahAnnounce = False
        schedule.every(adhaanCheckInterval).seconds.do(self.announceAdhaanAndSalah)
    def salahsToDate(self):
        for i in range(1,len(self.prayers)-2):
            for j in range(1,len(self.prayers[0])):
                salahsSplit = self.prayers[i][j].split(":")
                if i == 1:
                    self.prayerTimeObj[i-1][j-1] = datetime(year,month+1,day+1,int(salahsSplit[0]),int(salahsSplit[1]))
                else:
                    self.prayerTimeObj[i-1][j-1] = datetime(year,month+1,day+1,int(salahsSplit[0])+12,int(salahsSplit[1]))

    def showPrayers(self):
        height = len(self.prayers)
        width = len(self.prayers[0])

        for i in range(height): 
            for j in range(width): 
                if(i>0 and i<(height-2)) and j!=0:
                    self.prayerLabels[i-1][j-1]= Label(self.frame, text=self.prayers[i][j],background=frame1BgColor,font=("Arial",prayerFontSize),foreground="white")
                    self.prayerLabels[i-1][j-1].grid(row=i, column=j,ipadx=prayerLabelsPaddingX)
                else:
                    notPrayer =Label(self.frame, text=self.prayers[i][j],background=frame1BgColor,font=("Arial",prayerFontSize),foreground="white")
                    notPrayer.grid(row=i, column=j,ipadx=otherPrayerLabelsPaddingX)

    def checkPrayerPassed(self):
        setJamaah = False
        for i in range(len(self.prayerTimeObj)):
            if (self.prayerTimeObj[i][0]<datetime.now()):
                self.prayerLabels[i][0].config(background="green")
            if (self.prayerTimeObj[i][1]<datetime.now()):
                self.prayerLabels[i][1].config(background="red")
            if datetime.now()<self.prayerTimeObj[i][1] and not setJamaah:
                self.prayerLabels[i][1].config(background="green")
                setJamaah=True
                

        for i in range(len(self.prayerTimeObj)):
            if i == len(self.prayerTimeObj)-1:
                break
            if(self.prayerTimeObj[i+1][0]<datetime.now()):
                self.prayerLabels[i][0].config(background="red")
    def announceAdhaanAndSalah(self):
        for i in range(len(self.prayerTimeObj)):
            if(datetime.now() >= self.prayerTimeObj[i][0] and datetime.now() <(self.prayerTimeObj[i][0]+timedelta(minutes=1))) and not self.adhaanAnnounce:
                self.adhaanAnnounce = True
                self.startAnnounceIndex = i
                self.checkPrayerPassed()
                Thread(target=playNoise,args=("adhaan",)).start()
                break
            if(datetime.now() >= (self.prayerTimeObj[i][1] - timedelta(minutes=minsBeforeSalah)) and datetime.now() <(self.prayerTimeObj[i][1]-timedelta(minutes=(minsBeforeSalah-1))) and not self.salahAnnounce):
                self.salahAnnounce = True
                self.salahAnnounceIndex = i
                self.checkPrayerPassed()
                Thread(target=playNoise,args=("salah",)).start()
                break
        if not (datetime.now() >= self.prayerTimeObj[self.startAnnounceIndex][0] and datetime.now() <(self.prayerTimeObj[self.startAnnounceIndex][0]+timedelta(minutes=1))):
            self.adhaanAnnounce = False
        if not (datetime.now() >= (self.prayerTimeObj[self.salahAnnounceIndex][1] - timedelta(minutes=minsBeforeSalah)) and datetime.now() <(self.prayerTimeObj[self.salahAnnounceIndex][1]-timedelta(minutes=(minsBeforeSalah-1)))):
            self.salahAnnounce = False
