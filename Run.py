from tkinter import Tk,Label,Frame
from datetime import datetime
from Weather import Weather
from Settings import frame1BgColor,frame2BgColor,frame3BgColor,frame4BgColor,today,frame1Span,maxColumnSpan,clockFontSize,dateFontSize,notesTextFontSize,notesTitleFontSize,frame1PadY,frame2PadY,frame3PadY,frame4PadY
from Prayers import Prayers
from cec import *
from Ramadan import Ramadan
import os
import schedule
from cec import *
import time

switch_hdmi(2)
time.sleep(5)
root= Tk()


frame1 = Frame(root,background=frame1BgColor)
frame2 = Frame(root,background=frame2BgColor)
frame3 = Frame(root,background=frame3BgColor)
frame4 = Frame(root,background=frame4BgColor)


frame1.pack(ipady=frame1PadY)
frame2.pack(ipady=frame2PadY,fill="x")
frame4.pack(ipady=frame3PadY,side="bottom")
frame3.pack(ipady=frame4PadY,side="bottom")

Label(frame2,text="\n").pack(ipady=100)
errorMsgLabel = Label(frame2,text="Error, no internet connection",font=("Arial",notesTextFontSize+10),background=frame2BgColor,foreground="red")
r = Ramadan()
dayFrame = Frame(frame2,background=frame2BgColor)
sehriFrame = Frame(frame2,background=frame2BgColor)
iftaarFrame=Frame(frame2,background=frame2BgColor)
dayLabel = Label(dayFrame,text="Ramadan Day",font=("Arial",35),background=frame2BgColor,foreground="white")
day = Label(dayFrame,text=r.getRamadanDay(),font=("Arial",80),background=frame2BgColor,foreground="white")

sehriLabel = Label(sehriFrame,text="Sehri Ends",font=("Arial",35),background=frame2BgColor,foreground="white")
sehri = Label(sehriFrame,text=r.todaySehri,font=("Arial",80),background=frame2BgColor,foreground="white")

iftaarLabel = Label(iftaarFrame,text="Iftaar Starts",font=("Arial",35),background=frame2BgColor,foreground="white")
iftaar = Label(iftaarFrame,text=r.todayIftaar,font=("Arial",80),background=frame2BgColor,foreground="white")


dayLabel.pack()
day.pack()
sehriLabel.pack()
sehri.pack()
iftaarLabel.pack()
iftaar.pack()

dayFrame.pack(side="left",expand=True)
sehriFrame.pack(side="left",expand=True)
iftaarFrame.pack(side="right",expand=True)

p = Prayers(frame1,r.tmrroSehri,sehri,r.tmrroIftaar,iftaar)
# p = Prayers(frame1)
# Label(frame2,text="Notes",font=("Arial",notesTitleFontSize),background=frame4BgColor,foreground="white").pack(side='top')
try:
    w = Weather(frame3,errorMsgLabel)
except:
    w = None

# if today.strftime("%A") =="Friday":
#     Label(frame2,text="- Bid for house",font=("Arial",notesTextFontSize),background=frame2BgColor,foreground="white").pack()
Label(frame4,text=today.strftime('%A, %d %B %Y'),font=("Arial",dateFontSize),background=frame4BgColor,foreground="white").pack(side="bottom")
clock = Label(frame4,text=today.strftime('%I:%M:%S %p'),font=("Arial",clockFontSize),background=frame4BgColor,foreground="white")
clock.pack(side="bottom")


def repeater():
    time = datetime.now().strftime('%I:%M:%S %p')
    clock.config(text=time)
    if time == "12:00:00 AM":
        os.system("sudo reboot")
    schedule.run_pending()
    clock.after(200,repeater)

repeater()



root.config(bg=frame4BgColor)
root.attributes('-fullscreen',True)
root.mainloop() 

# GRID FORMAT IF NECESSARY
# frame1.grid(row=0, column=0, sticky="nsew",columnspan=frame1Span)
# frame2.grid(row=0, column=frame1Span, sticky="nsew",columnspan=(maxColumnSpan-frame1Span))
# frame3.grid(row=1, sticky="nsew",columnspan=maxColumnSpan)
# frame4.grid(row=2,  sticky="nsew",columnspan=maxColumnSpan)
# for i in range(maxColumnSpan):
#     root.grid_columnconfigure(i, weight=1, uniform="group1")
# root.grid_rowconfigure(0, weight=1)