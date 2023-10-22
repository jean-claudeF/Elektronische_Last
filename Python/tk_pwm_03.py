"""
tk_pwm_xx.py
 Connect to Raspi Pico with PWM program
 Sets PWM and frequency.
 
 Also general things:
 Uses picoconnector.py to get info about Picos and to distinguish them
 Can 
 display serial communication,
 reset / set REPL raw /set REPL normal,
 list files on Pico
 eventually send commands to the Pico
 
Debugging: comment out redirect as this hides some GUI errors 

"""    
import time
import tkinter as tk
import os
from tkinter.scrolledtext import ScrolledText
from terminalwindow_04 import Terminalwindow
from redirect_print_01 import Redirect
import picoconnector_02 as pconn
from buttonbar import Buttonbar, LabeledButtonbar
from listbox_dialog import MyListbox

#--------------------------------------------------------------------
''' SETTINGS 
     These can be edited by the user'''
comport = None
#debug = True 
debug = False
autoconnect = True
autoinit = True
startfreq = 16000


pwm_min = 0
pwm_max = 0.7
pwm_inc = 0.1
pwm_inc_small = 0.01
pwm_start = 0

freq_inc = 1000            # Hz
freq_min = 10000
freq_max = 20000

#----------------------------------------------------------------------

# Global variables not to be edited:
 
baud = 115200 
delay = 0 

freq = startfreq   
pwm_val = pwm_start

#----------------------------------------------------------------------

# Connection
    
def select_port():
    picos = pconn.scan_for_picos()
    #picos = pconn.pico_scan_with_info_strlist()
    print("Picos found:")

    for p in picos:
        print (p)

    pico = MyListbox("Picos found:", picos)
    print(pico)
    
    pico = pico.split(":")
    comport = pico[0].strip()
    return comport


def connect():
    disconnect()
    picos, picotext = pconn.scan_picoinfo()
    print(picotext)
    pico = MyListbox("Picos found:", picotext)
    print("Selected: ", pico)
    port = pico.split(" ")[0]
    print(port)
    
    serial_textbox.port = port
    serial_textbox.connect()

def select_and_init():
    connect()
    time.sleep(1)
    init()

def scan():
    pconn.scan_picoinfo() 

#-------------------------------------------------------------
'''General commands to pico'''

def sendcommand(cmd):
    #rawREPL()
    #t = serial_textbox.get('1.0', tk.END) +  "\r\n"
    serial_textbox.write(cmd.encode("utf8")) 
    serial_textbox.write(b'\x0D\x0A') 


def disconnect():
    serial_textbox.disconnect()
    
def clear():
    serial_textbox.delete('1.0', tk.END)
    '''
    redirect.back()
    txtbox.delete('1.0', tk.END)      # this does not work. Why???  I thought it had to do with redirect, but ist seems no
    txtbox.update()
    redirect.to(txtbox) 
    '''

    
def test():
    sendcommand("import os")
    sendcommand("os.listdir()")
    
    
def rawREPL():
    # Ctrl - A
    serial_textbox.write(b'\x01')     
    
def normalREPL():
    # Ctrl - B
    serial_textbox.write(b'\x02') 
    
def interrupt_program():
    # Ctrl - C
    serial_textbox.write(b'\x03\x03')
    
def soft_reset():
    # Ctrl - D
    serial_textbox.write(b'\x04')                          
    
def paste_mode():
    # Ctrl - E
    serial_textbox.write(b'\x05')    
    

def ls():
    serial_textbox.write("import os".encode("utf8"))
    serial_textbox.write(b'\x0D\x0A')
    serial_textbox.write("os.listdir()".encode("utf8") )
    serial_textbox.write(b'\x0D\x0A')    
        
#------------------------------------------------------------        

'''Specific PWM commands'''
# PWM

def init():
    import_pwmc()
    time.sleep(1)
    init_pwm(3, 16000)
    set_pwm(0)
    set_freq(startfreq)
     

def import_pwmc():
    cmd = "from pwmc import PWMc"
    sendcommand(cmd)

def init_pwm(pin, frequency):
    cmd = "pw = PWMc(" + str(pin) + ", freq= " + str(frequency) +")"
    sendcommand(cmd)
    

def set_pwm(pwmvalue):
    global pwm_val
    cmd = "pw.set_pwm(" + str(pwmvalue) + ")"
    sendcommand(cmd)
    pwm_val = pwmvalue
    pwmpercent = "%.1f" %(pwm_val * 100)
    lblpwm.configure(text = pwmpercent + "%")
    
def set_freq(frequency):
    global freq
    cmd = "pw.set_freq(" + str(frequency) + ")"
    sendcommand(cmd)
    freq = frequency
    lblfreq.configure(text = str(freq) + "Hz")
    
        
#------------------------------------------------------------------
# Frequency

def freq_plus():
    global freq
    freq += freq_inc
    if freq > freq_max:
        freq = freq_max
    set_freq(freq)
    
def freq_minus():
    global freq
    freq -= freq_inc
    if freq < freq_min:
        freq = freq_min
    set_freq(freq)
    
#---------------------------------------------------------------------
# PWM value



def pwm_plus():
    global pwm_val
    
    pwm_val +=  pwm_inc
    if pwm_val > pwm_max:
        pwm_val = pwm_max
    set_pwm(pwm_val)
           
def pwm_minus():
    global pwm_val
    
    pwm_val -=  pwm_inc
    if pwm_val < pwm_min:
        pwm_val = pwm_min
    set_pwm(pwm_val)

def pwm_stop():
    global pwm_val
    pwm_val = 0
    set_pwm(pwm_val)

def pwm_plus_small():
    global pwm_val
    
    pwm_val +=  pwm_inc_small
    if pwm_val > pwm_max:
        pwm_val = pwm_max
    set_pwm(pwm_val)

    
def pwm_minus_small():
    global pwm_val
    
    pwm_val -=  pwm_inc_small
    if pwm_val < pwm_min:
        pwm_val = pwm_min
    set_pwm(pwm_val)


    
#---------------------------------------------------------------------- 

    
    

    
    
#---------------------------------------------------- 


    
#--------------------------------------------------------------

if __name__ == "__main__": 
    
        
    
    cmds = {
            'Scan': scan,
            'Connect': select_and_init,
            'Clear': clear,
            'Raw REPL': rawREPL,
            'Normal REPL': normalREPL,
            'Stop program':interrupt_program,
            'Reset': soft_reset,
            'List files': ls,
            'Disconnect': disconnect,
            'Test': test,
    }     
    pwmcmds = { 'Init PWM': init,
                'Freq. +'+str(freq_inc): freq_plus,
                'Freq. -'+str(freq_inc): freq_minus,
                'PWM +'+str(pwm_inc): pwm_plus,
                'PWM -'+str(pwm_inc): pwm_minus,
                'PWM + '+str(pwm_inc_small): pwm_plus_small,
                'PWM - '+str(pwm_inc_small): pwm_minus_small,
                'PWM stop': pwm_stop,
              }  
    
    
    
    root = tk.Tk()
    root.title("Pico Connect")
    
    
    # Text boxes:
    frmtxt = tk.Frame(root)
    frmtxt.pack(side = tk.LEFT)
     
    lbl1 = tk.Label(text = "Serial communication:", master = frmtxt)
    lbl1.pack(side = tk.TOP)
    serial_textbox=Terminalwindow(comport, baud , master = frmtxt)      
    serial_textbox.pack()
    #serial_textbox.connect()
    
    lbl2 = tk.Label(text = "Program messages:", master = frmtxt)
    lbl2.pack(side = tk.TOP)
    
    txtbox = ScrolledText(master = frmtxt)
    txtbox.pack(side = tk.TOP)
    
    # Redirect system messages to lower textbox:
    if debug == False:
        redirect = Redirect()
        redirect.to(txtbox) 
        # In case of GUI problems set debug to True to see error messages
    
    
    # Commands:
    b2=LabeledButtonbar(cmds, "\n\nGeneral\ncommands",  labelside = tk.TOP, buttonside=tk.TOP)
    #b2.config(relief=tk.RIDGE, bd=3)
    b2.pack(side = tk.TOP)
    
    b3=LabeledButtonbar(pwmcmds, "\n\nPWM\ncommands",  labelside = tk.TOP, buttonside=tk.TOP)
    b3.pack()
    
    lblfreq = tk.Label(text = str(freq) + "Hz")
    lblfreq.pack()
    
    lblpwm = tk.Label(text = str(pwm_val * 100) + "%")
    lblpwm.pack()
    
    #connect()
    if autoconnect:
        connect()
    
    if autoinit:
        init()
    
    root.mainloop()
    
