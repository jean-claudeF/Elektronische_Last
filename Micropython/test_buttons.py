from machine import Pin
from blink import blink


btn1 = Pin(16, Pin.IN, Pin.PULL_UP)
btn2 = Pin(17, Pin.IN, Pin.PULL_UP)
led = Pin(18, Pin.OUT)

while True:
    if btn1.value() == 0:
        led.on()
        print("ON")
    else:
        led.off()
        
    if btn2.value() == 0:
        blink(2)
        
        