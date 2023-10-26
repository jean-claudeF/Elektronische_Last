''' Class PWMc allows setting of PWM 0 to 1   (0 to 100%)
    and changing frequency while keeping PWM value'''

from pwmc import PWMc
from machine import PWM, Pin, ADC, I2C
import time

from lcdlib import CharLCD

lcd = CharLCD(rs=16, en=17, d4=18, d5=19, d6=20, d7=21,
				  cols=8, rows=2)
# ADC
a0 = Pin(26, Pin.IN)				  # this is needed to turn input to high impedance
a1 = Pin(27, Pin.IN)				  # this is needed to turn input to high impedance
a2 = Pin(28, Pin.IN)
adc0 = ADC(0)		# Pin 31           Current I2
adc1 = ADC(1)		# Pin 32           Voltage V2
adc2 = ADC(2)       # Pin 34           
i2c_channel = 0
sclpin = 9
sdapin = 8
i2c = I2C(i2c_channel, scl=Pin(sclpin), sda=Pin(sdapin))

dac_pin = 13

# button:
button = Pin(2, Pin.IN, Pin.PULL_UP)

#-----------------------------------------------------------

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
    # sets I and returns measured voltage and current   
    cs.set_current(I)
    time.sleep(0.005)
    v = get_voltage(nb_mean = 5)
    i = get_current()
    return v, i

def set_and_print_IVP(I):
    # sets I, prints measured voltage, current, power
    cs.set_current(I)
    time.sleep(0.005)
    v = get_voltage(nb_mean = 5)
    i = get_current()
    p = v * i
    print(i, 'A\t', v, 'V\t',  p, 'W')

def lcd_values(V0, Pmax, Imax, Vmax):
    v0s = '%2.1fV' % V0
    pmaxs = '%3.1fW' % Pmax
    imaxs = '%2.1fA' % Imax
    vmaxs = '%2.1fV' % Vmax
    lcd.clear()
    lcd.message(pmaxs +" at " + imaxs)
    lcd.set_cursor(0, 1)
    lcd.message(vmaxs + "  V0="+ v0s)

def lcd_greeting():
    lcd.message("Solar analizer 4")
    lcd.set_cursor(0,1)
    lcd.message("Push button")

#--------------------------------------------------------

cs = CurrentSink(dac_pin, Rs = 0.22, freq = 1E6)

def measure_MPP(Imax_mA = 15100, Istep_mA = 100):

      
    Pmax = 0
    Vmax = 0
    Imax = 0
    
    # Get V0
    V0, I0 = set_and_measure(0) 
    
    print("I", '\t',  "V", '\t', "P",  '\t', "Im", '\t' , "Pm" )
    
    # Range in mA to avoid floating point
    for i in range(0, Imax_mA, Istep_mA):
        I = i/1000
        v, Im = set_and_measure(I)
        P = v * I
        Pm = v * Im
        print(I,'\t',  v,'\t', P, '\t', Im,'\t', Pm)
        if P > Pmax:
            Pmax = Pm
            Vmax = v
            Imax = Im
        #time.sleep(0.01)
        if v < 2.5:
            break
    set_and_measure(0)
    
    print('#')
    print('# V0 = %2.2f V' % V0)
    print('#')    
    print('# Pmax = %3.1f W' % Pmax)
    print('# Vmax = %2.2f V' % Vmax)
    print('# Imax = %2.2f A' % Imax)
    
    lcd_values(V0, Pmax, Imax, Vmax)

def main_loop():
    while True:    
        #measure_MPP()
        if button.value() == 0:
            time.sleep(0.1)
            measure_MPP(Istep_mA = 50)
            time.sleep(1)

#-------------------------------------------------------

# set_and_print_IVP(0)


if __name__ == '__main__':
    lcd_greeting()
    #measure_MPP(Istep_mA = 500)
    main_loop()
    
        

        

    
    
    
    
    

