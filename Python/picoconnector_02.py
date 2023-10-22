''' picoconnect_xx.py allows getting info about all connected Pico
and connecting to one special one.
See examples of use below
Developed by jean-claude.feltes@education.lu

Changed:
get_info_pico(pico, timeout=2)
Timeout should not be too short, otherwise some picos could be missed !!! 

scan_picoinfo():
   returns list with [portname, info]

'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
from serial.tools import list_ports
import time 


def scan_for_picos(verbose = True):
    '''returns list of USB portnames with Raspi Picos connected '''
    if verbose:
        print("Scanning for connected Picos")
    
    picos = []
    for port in list_ports.comports():
        if verbose:
            print("Checking ", port.device)
        if port.manufacturer != None:
            if verbose:
                print("Manufacturer: ", port.manufacturer)
            if "MicroPython" in port.manufacturer:
    
                picos.append(port.device)
    if verbose:
        print("Pico found on port:")
        for p in picos:
            print(p) 
        print()               
    return picos

#-----------------------------------------------------------------


def get_info_pico(pico, timeout=3, debug = False):
    '''
    Get info stored on the pico in a file info.txt
        This must contain a keyword in the first line:
        The keyword is returned  
    
    '''
    s=serial.Serial(pico, baudrate=115200)
    if s.isOpen()==False:
        s.open()
        
    flush_input_buffer(s)
    
    # send commands
    s.write(b'\x03\x03')        # Interrupt eventually running program
    s.write(b'\x02')            # Normal REPL
    s.write(b'f = open("info.txt", "r")\r')
    s.write(b't = f.readline()\r')
    s.write(b'f.close()\r')
    
    s.write(b'print("KEY=",t,"=ENDKEY")\r')
    
    
    time.sleep(0.1)     # Allow time to respond for the Pico
    
    t1 = time.time()
    text = ''
        
    while True: 
         nbbytes= s.inWaiting()
         c = s.read(nbbytes)
         c = c.decode("utf-8")
         text += c    
         if time.time()-t1 >timeout:
             break
         if text.find('=ENDKEY'):
             break 
             
    if debug:            
        print('RESPONSE: ', text)
        print("---")
    
    # Analize answer
    if 'Traceback' in text:                 # Something went wrong
        info = ''
    
    else:
        pos0 = text.find("KEY=")            # This is the print statement, not the right one
        pos1 = text.find("KEY=", pos0+ 1)   # This is the response 
        pos2 = text.find("=ENDKEY")         # This is the print statement, not the right one
        pos3 = text.find("=ENDKEY", pos2+1) # This is the right one
        info = text[pos1+len("KEY=")+1:pos3]
        info = info.strip()
        
    
    return info     

def flush_input_buffer(ser):
    n = ser.in_waiting
    ser.read(n) 
    
#-------------------------------------------------------------------------    

    
#---------------------------------------------------------------------- 
def scan_picoinfo():
    '''Print info on all picos connected
    returns picoinfo = list with [portname, info]
    amd picoinfo_text = list of textual descriptions
    '''
    picoinfo = []
    picoinfo_text = []
    print("Info on Picos found:")
    for pico_portname in scan_for_picos(verbose = False):
        info = get_info_pico(pico_portname)
        print (pico_portname, '  INFO:  ',   info)
        picoinfo.append([pico_portname, info])
        s = pico_portname + '  INFO:  ' +   info
        picoinfo_text.append(s)
    print()
    return picoinfo, picoinfo_text
#----------------------------------------------------------------------    
       
def find_pico(keyword, timeout = 1):
    '''returns name of the port where a Pico with the right keyword is connected'''
    picoportname = ''    
    for picoportname in scan_for_picos(verbose = False):
        info = get_info_pico(picoportname, timeout)
        if info == keyword:
            break
        
                
    return picoportname

#--------------------------------------------------------------------
def get_answer(port, timeout=0.2, verbose = True):
        t1 = time.time()
        text = ''
        while True:
            nbbytes = port.inWaiting()
            if nbbytes >0:
                c = port.read(nbbytes)
                c = c.decode("utf-8")
                text += c    
            if time.time() - t1 > timeout:
                break
        if verbose:
            print('RESPONSE: ', text)
        return text       
    
#-----------------------------------------------------------------------
class Pico():
    def __init__(self, keyword):
        self.keyword = keyword
        self.port = None
        self.portname = ""
        self.connected = False
        
    def connect(self, verbose = True):
        '''Connect to Pico with the right keyword
           (keyword in first line of file INFO.TXT on Pico'''
        self.portname = find_pico(self.keyword, 0.1)
        
        if self.portname:
            if verbose:
                print('Found ', self.keyword, ' on port',  self.portname)   

            self.port = serial.Serial(self.portname, baudrate = 115200)
            if self.port.open == False:
                self.port.open()
        else:
            if verbose:
                print(self.keyword + " not found")
            self.port = None        
               
        if self.port:
            self.connected = True
            if verbose:
                print ( "Connected to ", self.keyword)
                print()
    
    def reset(self):
        '''Reset Pico to restart in local mode'''
        print("Pico soft reset")
        self.port.write(b'\04')
        self.get_answer(timeout = 0.5)  
                    
    def set_rawREPL(self):
        # Ctrl - A
        self.port.write(b'\x01')     
    
    def set_normalREPL(self):
        # Ctrl - B
        self.port.write(b'\x02')    
        
    def close(self):
        '''Close connection to Pico'''
        if self.port:
            self.port.close()
    
    def interrupt_prog(self):
        if self.port:
            print("Interrupting running program\n")
            self.port.write(b'\x03\x03')
             
    def send_cmd(self, cmd, verbose = True, timeout = 1):
        '''send command to Pico
            cmd is a Python code line'''
        if verbose:
            print("CMD: ", cmd)
        self.port.write(cmd.encode('utf-8') + b'\r')
        
        self.get_answer()
           
        
        
    def get_answer(self, timeout=0.2, verbose = True):
        text = get_answer(self.port, timeout = timeout, verbose = verbose)
        return text    
      
    def list_files(self):
        '''Returns a list of the files on Pico '''
        self.send_cmd ("import os", timeout=2, verbose = False)
        time.sleep(1)
        self.send_cmd ("os.listdir()", timeout=2, verbose = False) 
        t = self.get_answer( timeout = 2, verbose = False)
        
        begin = t.find("[")
        t = t[t.find("[")+1:t.find("]")]
        t = t.replace(" ", "")
        t = t.replace("'", "")
        files = t.split(',')
        return files 
#--------------------------------------------------------------------------

''' TEST program: '''           
if __name__ == "__main__":
    
    ''' You can have info on all Picos connected'''
    scan_for_picos()
    
    picos = scan_picoinfo()
    for pico in picos:
        print (pico)
    
        
    '''You can connect to one special Pico
    This must contain the keyword in the first line of a file info.txt
    on the Pico'''
    keyword = 'PWMgenerator_02'
    mypico = Pico(keyword)
    mypico.connect()
    
    ''' The connected attribute tells if the connection was successful'''
    if mypico.connected:
        
        ''' You can interrupt a program (e.g. started by main.py at boot)
        or reset (reboot) the Pico'''
        mypico.reset()
        mypico.interrupt_prog()
        time.sleep(0.1)
        
        
        '''Commands can be sent and executed:'''
        #mypico.send_cmd("import time", verbose = False)
        #mypico.send_cmd("import time", verbose = True)
        mypico.set_rawREPL()
        mypico.send_cmd("3.14*5")
        print()
        print("Back to normal REPL")
        mypico.set_normalREPL()
        mypico.send_cmd("3.14*5")
        print()
        
        '''You can list the files on the Pico (except those in subfolders)'''
        print("Files on Pico:")
        files = mypico.list_files() 
        for f in files:
            print(f)
        
    
    '''Close the connection'''
    mypico.close()
    
    
