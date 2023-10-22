'''Set general commands like Reset, REPL etc. throug serial textbox
   serial_textbox variable must first be set with set_var()
'''  

from listbox_dialog import MyListbox
import picoconnector_02 as pconn
import time
 
def set_var(x):
    global serial_textbox
    serial_textbox = x
    

def sendcommand(cmd):
    #rawREPL()
    #t = serial_textbox.get('1.0', tk.END) +  "\r\n"
    serial_textbox.write(cmd.encode("utf8")) 
    serial_textbox.write(b'\x0D\x0A') 


def disconnect():
    serial_textbox.disconnect()
    


    
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

# Connection
    
def select_port():
    picos = pconn.scan_for_picos()
   
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
    
def auto_connect(keyword):
    disconnect()
    port = pconn.find_pico(keyword)
    
    serial_textbox.port = port
    serial_textbox.connect()


def scan():
    pconn.scan_picoinfo() 
