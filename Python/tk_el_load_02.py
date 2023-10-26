"""

TO DO: text -> array -> plot


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
import tkinter.filedialog as tkfd

from redirect_print_01 import Redirect
import picoconnector_02 as pconn
from buttonbar import Buttonbar, LabeledButtonbar
from listbox_dialog import MyListbox

# Serial textbox:
from terminalwindow_04 import Terminalwindow
from tk_pico_general import *     # General commands throug serial_textbox to pico
# !!! Remember to set_var(serial_textbox) as soon as serial_textbox is defined (below)  !!!

from text_to_plotscript_02 import *
import matplotlib.pyplot as plt  
import numpy as np
#--------------------------------------------------------------------
''' SETTINGS 
     These can be edited by the user'''
pico_key = "SOLAR_ANALYSER"    
comport = None
debug = False
#debug =True
autoconnect = True
autoinit = True

initcmd = "from solar_analyser_05 import measure_MPP"

#----------------------------------------------------------------------

# Global variables not to be edited:
 
baud = 115200 
delay = 0 
plotscript = ""
last_scriptfile = ""
#-------------------------------------------------------------
def text2xy(text, xcol, ycol, comment = '#'):
    """ returns numpy vectors x and y filled with data from text string
        data must be organized in columns separated by white space like TAB (0x09)
        xcol, ycol : column number for x and y values (starting from 0)  """
    
    lines=text.splitlines()
    i=0
    x=[]
    y=[]
       
    for line in lines:
        
        if len(line):
            if (line[0] != comment):
        
                columns = line.split()      #separator can be one or more " " or "\t"
                if len(columns)>=ycol:
                    data_error=0
                    try:
                        xl=float(columns[xcol])
                        
                    except:
                        data_error=1
                    
                    try:
                        yl=float(columns[ycol])
                    except:
                        data_error=2
                    
                    if data_error==0: 
                        x.append(xl)
                        y.append(yl)
                        i+=1
                        
                    else:
                        if debugflag:
                            print ("Data error in line ",i )   
                else:
                    if debugflag:
                        print ("Unsufficient data in line",i)    
    
    x=np.array(x)
    y=np.array(y) 
    return x,y        
#-------------------------------------------------------------
def pythonise_vector(xvector, xname):
    '''returns a Python line defining the vector
    e.g. "x = [0, 2.3, 5.6, ....]
    This line can be executed together with other Python statements'''
    s = xname +" = ["
    for xx in xvector:
        s+=  str(xx) + ", " 
    s += "]"    
    return s
#---------------------------------------------------------------    


#-----------------------------------------------------------------

template =  """
import matplotlib.pyplot as plt
fig1 = plt.figure()

ax1 = fig1.add_subplot(211)
l1, = ax1.plot (I,V)
plt.ylabel('U/V')

ax2 = fig1.add_subplot(212)
l2, = ax2.plot (I,P)
plt.ylabel('P/W')

plt.xlabel('I/A')

# plt.grid(True)
# plt.xlim(xmin, xmax)
# plt.ylim(ymin, ymax)
plt.show()
""" 


def make_plotscript(vectors):
    ''' Make executable Python script out of data vectors
    '''
    s = vectors
    s += template  
    return s    

#----------------------------------------------------------------

        
#------------------------------------------------------------        

'''Specific commands'''
def select_and_init():
    connect()
    time.sleep(1)
    init()

def init():
   
    sendcommand(initcmd)
   
def measure():
    clear()
    ###global r1, c1
    ###r1, c1 = get_col_row(serial_textbox)
    cmd = "measure_MPP(Istep_mA = 50)"
    sendcommand(cmd)   

def extract_data():
    t=serial_textbox.get("1.0", tk.END)	#
   
    ts = ""
    if len(t)>1:
        tl = t.splitlines()
        tl = tl[1:-5]
        for s in tl: 
            ts += s + '\n'
    print (ts)
    root.clipboard_append(ts, type = "STRING")
    print ("Data copied to clipboard") 
    return ts   
    
def plot():
    global plotscript
    # Use current set values
    t = extract_data()
    print(t)
    I, V = text2xy(t, 0, 1)
    _, P = text2xy(t, 0, 2)  
    
    Ipy = pythonise_vector(I, "I")
    Vpy = pythonise_vector(V, "V")
    Ppy = pythonise_vector(P, "P")
    
    vectors = Ipy +'\n' + Vpy + '\n' + Ppy + '\n'
    
    plotscript = make_plotscript(vectors)
    print()
    print(plotscript)
    exec(plotscript)
     
    
   
def plot2():
    # Use current measured values
    # Mostly gives better result
    global plotscript
    t = extract_data()
    print(t)
    I, V = text2xy(t, 3, 1)
    I, P = text2xy(t, 3, 4)  
    
    Ipy = pythonise_vector(I, "I")
    Vpy = pythonise_vector(V, "V")
    Ppy = pythonise_vector(P, "P")
    
    vectors = Ipy +'\n' + Vpy + '\n' + Ppy + '\n'
    
    plotscript = make_plotscript(vectors)
    print()
    print(plotscript)
    exec(plotscript) 


def measure_and_plot():
    measure()
    root.after(2000, plot)
    
def measure_and_plot2():
    measure()
    root.after(2000, plot2)    
           
    
#--------------------------------------------------------------
#    GUI functions

def get_col_row(textctrl):
    index = textctrl.index('insert')
    index = index.split(".")
    col=index[1]
    row=index[0]
    
    return col, row 


def clear():
    serial_textbox.delete('1.0', tk.END)
   

def save_script():
    global plotscript
    filename=tkfd.asksaveasfilename(filetypes = (("dat.py files","*.dat.py"),))
    if filename is not None:
        if filename[-7:] != '.dat.py':
            filename += '.dat.py'

        with open(filename, 'w') as f:
            
            f.write(plotscript)     
            f.close()
        last_scriptfile = filename

plotscript = "" 
           
def load_script():
    
    global plotscript
    filename=tkfd.askopenfilename(filetypes = (("dat.py files","*.dat.py"),))
    if filename is not None:
        with open(filename, 'r') as f:
            plotscript = f.read()
            f.close()
        exec(plotscript)
        last_scriptfile = filename



simple_interface = True
# simple_interface = False


if __name__ == "__main__": 
    
    cmds = {
            'Scan': scan,
            'Connect': select_and_init,
            'Raw REPL': rawREPL,
            'Normal REPL': normalREPL,
            'Stop program':interrupt_program,
            'Reset': soft_reset,
            'List files': ls,
            'Disconnect': disconnect,
            
             } 
             
    
                     
    pwmcmds = { 'Init': init,
                'Measure': measure,
                'Clear': clear, 
                'Plot': plot,
                'Measure + plot\nUse set I': measure_and_plot,
                'Measure + plot\nUse measured I': measure_and_plot2,
              }  
    
    
    if simple_interface:
        cmds = {
            'Normal REPL': normalREPL,
            'Stop program':interrupt_program,
            'Reset': soft_reset,
            'Disconnect': disconnect,
            
             } 
             
    
                     
        pwmcmds = {
                
                'Measure + plot': measure_and_plot2,
                'Save': save_script,
                'Load': load_script,
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
    set_var(serial_textbox)
    
    
    lbl2 = tk.Label(text = "Program messages:", master = frmtxt)
    lbl2.pack(side = tk.TOP)
    txtbox = ScrolledText(master = frmtxt, height=5)
    txtbox.pack(side = tk.TOP)
    
    # Eventually redirect system messages to lower textbox, if debug = False:
    if debug == False:
        redirect = Redirect()
        redirect.to(txtbox) 
        # In case of GUI problems set debug to True to see error messages
    
    
    # Commands:
    b2=LabeledButtonbar(cmds, "\n\nGeneral\ncommands",  labelside = tk.TOP, buttonside=tk.TOP)
    #b2.config(relief=tk.RIDGE, bd=3)
    b2.pack(side = tk.TOP)
    
    b3=LabeledButtonbar(pwmcmds, "\n\nMPP\ncommands",  labelside = tk.TOP, buttonside=tk.TOP)
    b3.pack()
    
        
    #connect()
    if autoconnect:
        auto_connect(pico_key)
    
    if autoinit:
        init()
    
    root.mainloop()
    
