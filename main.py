# MicroPython TM1637 quad 7-segment LED display driver examples

# WeMos D1 Mini -- 4 Digit Display
# D1 (GPIO5) ----- CLK
# D2 (GPIO4) ----- DIO
# 3V3 ------------ VCC
# G -------------- GND
from machine import Pin,RTC
import time,tm1637,ntptime,ds18b20#onewire,network
tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))#


cal_year=0
cal_mon=0
cal_day=0
cal_hour=0
cal_min=0
cal_sec=0

server=['ntp.tencent.com',
        'ntp1.tencent.com',
        'ntp2.tencent.com',
        'ntp3.tencent.com',
        'ntp4.tencent.com',
        'ntp5.tencent.com']
if __name__ == "__main__":
    
    tm.brightness(1)    #
    ntptime.NTP_DELTA = 28800   #
    ntptime.host = 'ntp.tencent.com'    #
    try:
        ntptime.settime()    #
    except ETIMEOUT:
        ntptime.host='ntp4.tencent.com'
    rtc=RTC()
    print(rtc.datetime())
    time.sleep(1)
    sensor=ds18b20.ds(2,'c',9) #creates sensor object set to default pin 2, units in Celcius, resolution 12 bit
    #sensor.addr, sensor.pin, sensor.unit, and sensor.res values are now available
    #you can change the object parameters by the following:
    #pin number - sensor.pin=[number]
    #unit - sensor.unit=['c'|'f']
    #resolution - sensor.res=[9|10|11|12]
    while True:
        for j in range(20):#NTP per 10mins
            try:
                ntptime.settime()    #
            except ETIMEOUT:
                ntptime.host='ntp4.tencent.com'
            rtc=RTC()
            list_time = time.localtime()    #
            #cal_year = list_time[0]    #
            #cal_mon = list_time[1]
            #cal_day = list_time[2]
            cal_hour = list_time[3]+8
            while cal_hour>24:
                cal_hour=cal_hour-24
            if cal_hour==24:
                tm.show('    ')
                for k in range(8):
                    time.sleep(3600)
            cal_min = list_time[4]
            #raw_min = list_time[4]
            cal_sec = list_time[5]
            for  i in range (25):
                tm.numbers(cal_hour,cal_min,True)    #
                #print(list_time)    #
                time.sleep(0.5)    #
                tm.numbers(cal_hour, cal_min,False)    #
                time.sleep(0.5) 
            temp=ds18b20.read(sensor)
            tm.temperature(int(temp[0]))
            time.sleep(5)

            



            


