
def set_var(x):
    global serial_textbox
    serial_textbox = x
    print(serial_textbox)

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
