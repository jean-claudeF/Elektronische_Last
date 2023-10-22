''' Class PWMc allows setting of PWM 0 to 1   (0 to 100%)
    and changing frequency while keeping PWM value'''

from machine import PWM, Pin, ADC, I2C
import time

# ADC
a0 = Pin(26, Pin.IN)				  # this is needed to turn input to high impedance
a1 = Pin(27, Pin.IN)				  # this is needed to turn input to high impedance
a2 = Pin(28, Pin.IN)
adc0 = ADC(0)		# Pin 31           Current I2
adc1 = ADC(1)		# Pin 32           Voltage V2
adc2 = ADC(2)       # Pin 34           Manual PWM pot
i2c_channel = 0
sclpin = 9
sdapin = 8
i2c = I2C(i2c_channel, scl=Pin(sclpin), sda=Pin(sdapin))

dac_pin = 13

class PWMc:
    def __init__(self, pin, freq = 5000):
        # set PWM pin + frequency
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(int(freq))
        self.pwm.duty_u16(0)
        
        
    def set_pwm(self, value):
        # set PWM value 0.0 to  1.0, returns integer value 0...65535 corresponding to PWM
        self.value = value                 # remember last value
        pwmval = int(65535 * value)
        if pwmval > 65535: pwmval = 65535
        if pwmval < 0: pwmval = 0
        self.pwm.duty_u16(pwmval)
        return pwmval
    
     
    def set_freq(self, freq):
        # set new PWM frequency without changing the PWM value, returns frequency
        self.pwm.freq(int(freq))
        self.set_pwm(self.value)
        return self.pwm.freq()
        
    def stop(self):
        # deinit PWM
        self.set_pwm(0)
        self.pwm.deinit()

    def set_dac(self, v):
        self.set_pwm(v/3.3)

#-----------------------------------------------------------

class CurrentSink(PWMc):
    def __init__(self, pin, Rs = 0.22, freq = 1E6):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(int(freq))
        self.pwm.duty_u16(0)
        self.Rs = Rs
        self.ki = .9191176
    
    def set_current(self, I):
        self.set_dac(self.Rs * I * self.ki)

#----------------------------------------------------------
def get_voltage(nb_mean = 3, k = 18.67):
    v = 0
    for i in range(0, nb_mean):
        v += adc1.read_u16()
    v = v/nb_mean * (3.3 / 65535) 
    v = v * k
    return v

def set_and_measure(I):
    # sets I and returns voltage    
    cs.set_current(I)
    time.sleep(0.005)
    v = get_voltage(nb_mean = 5)
    return v
#--------------------------------------------------------

cs = CurrentSink(dac_pin, Rs = 0.22, freq = 1E6)

def measure_MPP(Imax_mA = 15100, Istep_mA = 100):

      
    Pmax = 0
    Vmax = 0
    Imax = 0
    
    # Range in mA to avoid floating point
    for i in range(0, Imax_mA, Istep_mA):
        I = i/1000
        v = set_and_measure(I)
        P = v * I
        print(I, v, P)
        if P > Pmax:
            Pmax = P
            Vmax = v
            Imax = I
        #time.sleep(0.01)
        if v < 2.5:
            break
    set_and_measure(0)
    
    print('#')
    print('# Pmax = %3.1f W' % Pmax)
    print('# Vmax = %2.2f V' % Vmax)
    print('# Imax = %2.2f A' % Imax)
    
    

if __name__ == '__main__':
    
    measure_MPP()
    measure_MPP(Istep_mA = 50)
    

        

    
    
    
    
    



