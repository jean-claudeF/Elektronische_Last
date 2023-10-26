''' Electronic current sink'''

from machine import PWM, Pin, ADC
from pwmc import PWMc
import time

a0 = Pin(26, Pin.IN)				  # this is needed to turn input to high impedance
a1 = Pin(27, Pin.IN)				  # this is needed to turn input to high impedance
a2 = Pin(28, Pin.IN)
adc0 = ADC(0)		# Pin 31           Current I2
adc1 = ADC(1)		# Pin 32           Voltage V2
adc2 = ADC(2)       # Pin 34               


class CurrentSink(PWMc):
    def __init__(self, pin, Rs = 0.22, freq = 1E6):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(int(freq))
        self.pwm.duty_u16(0)
        self.Rs = Rs
        self.ki = .9191176
    
    def set_dac(self, v):
        self.set_pwm(v/3.3)

    def set_current(self, I):
        self.set_dac(self.Rs * I * self.ki)

#----------------------------------------------------------
def get_voltage(nb_mean = 5, k = 18.67):
    v = 0
    for i in range(0, nb_mean):
        v += adc1.read_u16()
    v = v/nb_mean * (3.3 / 65535) 
    v = v * k
    return v

def get_current(nb_mean = 5, k = .22 * .9191176):
    v = 0
    for i in range(0, nb_mean):
        v += adc0.read_u16()
    v = v/nb_mean * (3.3 / 65535) 
    v = v / k
    return v

def set_and_measure(I):
    # sets I and returns voltage    
    cs.set_current(I)
    time.sleep(0.005)
    v = get_voltage(nb_mean = 5)
    i = get_current()
    return v, i


if __name__ == '__main__':
    print("Start PWM on GPIO 13, 200kHz, 60%")
    #pw = PWMc(13, freq= 1000E3)
    cs = CurrentSink(13, freq = 1E6)
    
    for I in range(0,7):
        v, Im = set_and_measure(I)
        print(I, ' \t', Im, '\t',  v)
        time.sleep(4)
    cs.set_current(0)
    
    
    
    
    
    
    



