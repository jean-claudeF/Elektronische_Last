''' Class PWMc allows setting of PWM 0 to 1   (0 to 100%)
    and changing frequency while keeping PWM value
    
    set_dac is a function to output analog signals
    (needs low pass filter + impedance converter)
    '''

from machine import PWM, Pin

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


    
    
        
if __name__ == '__main__':
    print("Start PWM on GPIO 13, 200kHz, 60%")
    pw = PWMc(13, freq= 1E6)
    
    pw.set_dac(1)
    
    '''
    while True:
        for i in range(0,100):
            p = i /100
            pw.set_pwm(p)
            
    '''
    
    
    
    
    
    



