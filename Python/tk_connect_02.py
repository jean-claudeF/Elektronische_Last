"""
tk_connect_xx.py
 Connect to Raspi Pico.
 Uses picoconnector.py to get info about Picos and to distinguisgh them
 Can 
 display serial communication,
 reset / set REPL raw /set REPL normal,
 list files on Pico
 eventually send commands to the Pico
 
Debugging: comment out redirect as this hides some errors 

"""    
import time
import tkinter as tk
import os
from tkinter.scrolledtext import ScrolledText
from terminalwindow_04 import Terminalwindow
from redirect_print_01 import Redirect
import picoconnector_02 as pconn
from buttonbar import Buttonbar
from listbox_dialog import MyListbox

#---------------------------------------------------------------------- 
'''General commands to pico'''


def do_cmds(picocmds):
    for cmd in picocmds:
        print(cmd)
        pc.cmd_to_pico(ser, cmd)
        
#------------------------------------------------------------        

'''Specific PWM commands'''
def import_pwmc():
    cmd = "from pwmc import PWMc"
    mypico.send_cmd(cmd)

def init_pwm(pin, frequency):
    cmd = "pw = PWMc(" + str(pin) + ", freq= " + str(frequency) +")"
    mypico.send_cmd(cmd)
    

def set_pwm(pwmvalue):
    cmd = "pw.set_pwm(" + str(pwmvalue) + ")"
    mypico.send_cmd(cmd)
    
    
def set_freq(frequency):
    cmd = "pw.set_freq(" + str(frequency) + ")"
    mypico.send_cmd(cmd)
        

def set10kHz():
    set_freq(10000)
    
def set12kHz():
    set_freq(12000)

#---------------------------------------------------------------------- 


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
    
def send():
    #rawREPL()
    t = cmd_textbox.get('1.0', tk.END) +  "\r\n"
    for line in t.splitlines():
        line = line + '\n'
        serial_textbox.write(line.encode("utf8")) 
        serial_textbox.write(b'\x0D\x0A') 
    #normalREPL()     
    
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
    
    
def scan():
    pconn.scan_picoinfo() 
    
    
#---------------------------------------------------- 

baud = 115200 
delay = 0 
   
    
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
    
#--------------------------------------------------------------

if __name__ == "__main__":  
    
    cmds = {
            'Scan': scan,
            'Connect': connect,
            'Clear': clear,
            'Raw REPL': rawREPL,
            'Normal REPL': normalREPL,
            'Stop program':interrupt_program,
            'Reset': soft_reset,
            'List files': ls,
            'Disconnect': disconnect
    }     
    pwmcmds = {
                '10kHz': set10kHz,
                '12kHz': set12kHz,
              }  
    
    
    
    mainwindow = tk.Tk()
    mainwindow.title("Pico Connect")
    comport = None
    
    lbl1 = tk.Label(text = "Serial communication:", master = mainwindow)
    lbl1.pack(side = tk.TOP)
    serial_textbox=Terminalwindow(comport, baud , master = mainwindow)      
    serial_textbox.pack()
    #serial_textbox.connect()
    
    b2=Buttonbar(cmds, side=tk.LEFT)
    b2.config(relief=tk.RIDGE, bd=3)
    b2.pack(side = tk.TOP)
    
    lbl2 = tk.Label(text = "Program messages:", master = mainwindow)
    lbl2.pack(side = tk.TOP)
    
    txtbox = ScrolledText(master = mainwindow)
    txtbox.pack(side = tk.TOP)
    
    redirect = Redirect()
    redirect.to(txtbox) 
    
    b3 = Buttonbar(pwmcmds, side = tk.LEFT)
    b3.pack()
    
    
    #connect()
    
    mainwindow.mainloop()
    
