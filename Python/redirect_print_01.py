
'''Tkinter Redirect print to textbox'''
# https://stackoverflow.com/questions/12351786/how-to-redirect-print-statements-to-tkinter-text-widget
'''What he did was that he assigned sys.stdout to Class TextRedirector with a Method .write(str)
so calling print('string') -calls for-> sys.stdout.write('string') -callsfor-> TextRedirector.write('string') 
'''

import tkinter as tk
import sys
#import redirect_print_01 as redirect
  
    
#-----------------------------------------------------------------------

old_stdout = sys.stdout
old_stderr = sys.stderr


class _TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag
        
        
        self.old_stderr = sys.stderr

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
        self.widget.update()

class Redirect():
    def __init__(self):
        self.old_stdout = sys.stdout
        self.oldstderr = sys.stderr
        
        
    def to(self, txtbox):
        # redirect print and error to txtbox
        sys.stdout = _TextRedirector(txtbox, "stdout")
        sys.stderr = _TextRedirector(txtbox, "stderr")


    def back(self):
        sys.stdout = self.old_stdout
        sys.stderr = self.oldstderr
        
        



#----------------------------------------------------------------------

''' Sample program'''







if __name__ == "__main__":
    
    redirect = Redirect()
    
    
    def print_to_txtbox():
        redirect.to(txtbox)
        
    def print_normal():
        redirect.back()
        

    
    
    
    def do_some_print():
        '''Illustrate that using 'print' writes to stdout'''
        print ("this is stdout")
        print(eval("3+5"))

    def do_errormessage():
        '''Illustrate that we can write directly to stderr'''
        sys.stderr.write("this is stderr\n")
        print(eval("3+-*/5"))
    
    
    
    
    root = tk.Tk()
    toolbar = tk.Frame()
    toolbar.pack(side="top", fill="x")
    
    b1 = tk.Button(toolbar, text="print to stdout", command = do_some_print)
    b2 = tk.Button(toolbar, text="print to stderr", command = do_errormessage)
    b3 = tk.Button(toolbar, text="Redirect", command = print_to_txtbox)
    b4 = tk.Button(toolbar, text="Undo redirect", command = print_normal)
    b1.pack( side="left")
    b2.pack( side="left")
    b3.pack( side="left")
    b4.pack( side="left")
    
    txtbox = tk.Text( wrap="word")
    txtbox.pack(side="top", fill="both", expand=True)
    txtbox.tag_configure("stderr", foreground="#b22222")

    
    
    root.mainloop()

