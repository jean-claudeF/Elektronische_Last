''' TEST program: '''           
#from picoconnector_01 import scan_for_picos, scan_picoinfo, Pico
from picoconnector_02 import scan_for_picos, scan_picoinfo, Pico
import time


if __name__ == "__main__":
    
    ''' You can have info on all Picos connected'''
    #picos = scan_for_picos()
    
        
    picos = scan_picoinfo()
    for pico in picos:
        print (pico)
    
    '''You can connect to one special Pico
    This must contain the keyword in the first line of a file info.txt
    on the Pico'''
    keyword = 'PWMgenerator_02'
    ##keyword = ''      #-> first Pico found with or without info.txt
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
    
    
