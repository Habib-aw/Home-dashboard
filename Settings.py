from datetime import datetime

maxColumnSpan=7
frame1Span = 4

frame1BgColor= "black"
frame2BgColor= "black"
frame3BgColor= "black"
frame4BgColor= "black"

firstJammahSummer = "1:30"
secondJammahSummer = "1:50"

firstJammahWinter = "1:00"
secondJammahWinter = "1:20"

today = datetime.today()
month= today.month-1
day = today.day-1
year = today.year
minsBeforeSalah = 25
prayerFontSize = 30

hourlyWeatherIconWidth= 50
hourlyWeatherIconHeight= 50
dailyWeatherIconHeight= 50
dailyWeatherIconWidth= 50
hourlyWeatherDataFontSize = 20
hourlyWeatherHeadingFontSize = 15
dailyDayFontSize = 15
dailyTempFontSize = 25

notesTitleFontSize = 53
notesTextFontSize = 30
dateFontSize = 53
clockFontSize = 53
numOfWeatherHours = 7

hourlyWeatherPaddingX=0
forecastsPaddingX=0
prayerLabelsPaddingX = 36
otherPrayerLabelsPaddingX = 0


hourWeatherCheckInterval = 10 #min
adhaanCheckInterval = 1 # sec
prayerPassedCheckInterval =1 # min

frame1PadY = 0
frame2PadY = 0
frame3PadY = 0
frame4PadY = 0