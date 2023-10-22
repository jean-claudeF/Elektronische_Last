''' Electronic current sink'''

from machine import PWM, Pin
from pwmc import PWMc


    


class CurrentSink(PWMc):
    def __init__(self, pin, Rs = 0.22, freq = 100E3):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(int(freq))
        self.pwm.duty_u16(0)
        self.Rs = Rs
        self.ki = .9191176
        
    def set_dac(self, v):
        self.set_pwm(v/3.3)
        
    def set_current(self, I):
        self.set_dac(self.Rs * I * self.ki)
        
if __name__ == '__main__':
    print("Start PWM on GPIO 13, 200kHz, 60%")
    #pw = PWMc(13, freq= 1000E3)
    cs = CurrentSink(13, freq = 1E6)
    
    cs.set_dac(2)
    #cs.set_current(.5)
    
    
    '''
    while True:
        for i in range(0,100):
            p = i /100
            pw.set_pwm(p)
            
    '''
    
    
    
    
    
    



