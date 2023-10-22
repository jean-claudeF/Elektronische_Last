# text_to_plotscript_0x
"""
make_plotscript(datatext) turns tabular data into executable Python code
datatext must be a CSV string with '\t' as separator
col0 is for x data,
col1,2... for y data
Needs numpy, matplotlib, StringIO
"""

from io import StringIO
import numpy as np

debugflag=True
#-----------------------------------------------------------------------
def analyse_data(text, max_test_lines = 20, comment = '#' ):
    # How many valid data columns does the text have?
    # returns minimum number of columns
    
    nb_cols = []
    
    lines=text.splitlines()
    
    
    
    nb_lines = len(lines)
    print("Number of lines: ", nb_lines)
    
    if nb_lines < max_test_lines:
        max_test_lines = nb_lines
        
    for i in range(0, max_test_lines):
        line = lines[i]
        if len(line):
            if (line[0] != comment):
                cols = line.split()
                cols = len(cols)
                ##print("Line ", i, ": ", cols)
                nb_cols.append(cols)
    
    nb_cols = np.array(nb_cols)
    min_cols = min(nb_cols)
    max_cols = max(nb_cols)
    
    print ("Min. nb of cols: ", min_cols)
    print ("Max. nb of cols: ", max_cols)            
            
    return min_cols    
    
#-----------------------------------------------------------------------        
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
#--------------------------------------------------------------------------
def xy2text(x, y):
        """ returns arrays x and y to a  text string with columns separated by <TAB>"""
        i=0
        t=""
        for x1 in x:
           line= str( x[i]) + "\t" + str( y[i]) +"\n"
           i+=1
           t = t+ line
        return t      
#-------------------------------------------------------------------------
def string2xy(text, xcol, ycol):
    """ returns vectors x and y filled with data from text string
        data must be organized in columns separated by white space like TAB (0x09)
        xcol, ycol : column number for x and y values (starting from 0)  
        uses numpy.genfromtxt function""" 
    data=StringIO(text)
    a = np.genfromtxt(data, invalid_raise=False)
    #a = np.genfromtxt(data)
    #a=np.loadtxt(data)
    x=a[:,xcol]
    y=a[:,ycol]
    return x,y
#----------------------------------------------------------------------- 
def string2matrix(text):
    """ Turns string data into a matrix"""
    data=StringIO(text)
    a = np.genfromtxt(data, invalid_raise=False)
    print(a.shape)
    nbcols = a.shape[1]
    nbrows = a.shape[0]
    print( nbcols, " columns")
    print(nbrows, " rows")
    return a, nbcols, nbrows
 
#-----------------------------------------------------------------------
def string2vectors(text):
    """returns list of numpy arrays with column data
    [col0data, col1data ...]
    """
    a, nbcols, nbrows = string2matrix(text) 
        
    z = []
    for i in range(0, nbcols ):
        z.append( a[:, i]) 
        
    return z, nbcols    

#-----------------------------------------------------------------------

def pythonise_vector(xvector, xname):
    '''returns a Python line defining the vector
    e.g. "x = [0, 2.3, 5.6, ....]
    This line can be executed together with other Python statements'''
    s = xname +" = ["
    for xx in xvector:
        s+=  str(xx) + ", " 
    s += "]"    
    return s

def pythonise_text(datatext):
    '''returns Python lines defining the column vectors
    names: 
        col 0 -> x
        col 1, 2...  -> y1, y2 ...'''
    names = []
    columndata, nbcols = string2vectors(datatext)
    
    # col0 -> x:
    col0name = 'x'
    names.append(col0name)
    sx = pythonise_vector(columndata[0], col0name) + '\n'
    
    # next cols -> y:
    sy = ""
    
    for i in range(1, nbcols):
        name = "y" + str(i) 
        names.append(name)
        sy += pythonise_vector(columndata[i], name) + '\n'
        
    py_lines = sx + sy    
    return  py_lines, names 

def make_plotscript(datatext):
    ''' Make executable Python script out of data in tabular form
    The script plots the data with matplotlib
    x = col0
    y = col 1, 2...
    '''
  
    py_vectors, names  = pythonise_text(datatext)
    
    
    s = "\nimport matplotlib.pyplot as plt\n"
    s += "fig1 = plt.figure()\n"
    s += "ax1 = fig1.add_subplot(111)\n\n"  
    
    s += py_vectors + '\n'
    
    xname = names[0]
    ynames = names[1:]
    
    # plot
    i = 1
    linenames = []
    for yname in ynames:
        linename = "l" + str(i) 
        s += linename + ", = ax1.plot (" + xname + "," + yname + ")\n"
        linenames.append(linename)
        i += 1
    
    s += "\n# Edit here if you want:\n"   
    for linename in linenames:
         s += '#' + linename + ".set_color('blue')\n"
        
    s += "plt.xlabel('x')\n"
    s += "plt.ylabel('y')\n" 
    s += "# plt.grid(True)\n"  
    s += "# plt.xlim(xmin, xmax)\n"
    s += "# plt.ylim(ymin, ymax)\n"
    
    s += "plt.show()"
    
    return s    
        
#------------------------------------------------------------------------

if __name__ == '__main__':
   
    # Main test program 

    testdata1 ="""
    # title
    0.792   0.01    0.11    0.23    0.20
    0.796   0.01    0.10    0.20    0.20
    0.800   0.01    0.10    0.20    0.20
    0.804   5.09    0.76    0.47    
    0.808   5.08    2.85    2.28    1.98
    0.812   5.09    3.69    3.31    3.10
    0.816   5.09    4.15    3.93    3.75
    0.820   5.09    4.41    4.26    4.11
    0.824   5.10    4.55    4.43    4.32
    0.828   5.09    4.64    4.52    4.43
    0.832   5.10    4.67    4.61    4.49
    0.836   5.08    4.70    4.64    4.52
    0.840   5.08    4.72    4.64    4.55
    0.844   5.09    4.74    4.67    4.55
    0.848   5.10    4.74    4.67    4.55
    0.852   5.10    4.75    4.67    4.55
    0.856   0.01    2.68    3.40    3.61
    0.860   0.01    1.50    2.01    2.13
    0.864   0.01    0.88    1.24    1.30
    0.868   0.01    0.54    0.80    0.80
    0.872   0.01    0.34    0.53    0.53
    0.876   0.00    0.24    0.38    0.38
    0.880   0.00    0.17    0.32    0.29
    0.884   0.01    0.14    0.26    0.26
    0.888   0.00    0.12    0.23    0.23
    0.892   0.01    0.11    0.23    0.20
    0.896   0.01    0.10    0.20    0.20
    0.900   0.01    0.10    0.20    0.20
    0.904   5.09    0.86    0.53    0.35
    0.908   5.09    2.88    2.30    2.01
    0.912   5.09    3.70    3.34    3.13
    0.916   5.09    4.16    3.93    3.75
    0.920   5.09    4.42    4.26    4.11
    0.924   5.08    4.55    4.43    4.32
    0.928   5.08    4.63    4.55    4.40
    0.932   5.09    4.68    4.61    4.49
    0.936   5.09    4.71    4.61    4.52
    0.940   5.09    4.72    4.64    4.55
    0.944   5.09    4.74    4.67    4.55
    0.948   5.09    4.74    4.67    4.55
    0.952   5.09    4.75    4.67    4.58
    0.956           2.64    3.37    3.58
    0.960   0.01    1.48    1.98    2.13
    0.964   0.01    0.88    1.21    1.27
    0.968   0.01    0.53    0.77    0.80
    0.972   0.01    0.35    0.53    0.53
    0.976   0.01    0.24    0.38    0.38
    0.980   0.00    0.17    0.32    0.29
    0.984   0.01    0.14    0.26    0.26
    0.988   0.01    0.12    0.23    0.23
    0.992   0.01    0.11    0.23    0.20
    """
    testdata2 ="""
    2	08:32:35_T_27.10.21	0.00250	0.00513	0.00000	0.00400
    3	08:32:36_T_27.10.21	0.00263	0.00588	0.00000	0.00538
    4	08:32:37_T_27.10.21	0.00275	0.00550	-0.00013	0.00638

    """
    #testdata=testdata *1000
    testdata = testdata1



    def demo1(testdata):
        nb_cols = analyse_data(testdata)    
            
        for i in range(1,nb_cols):
            x,y = text2xy(testdata, 0,i) 
            #x, y = string2xy(testdata, 0,i)
            print(x)
            print(y)
            plt.plot(x,y)
        
        plt.show()

    def demo2(testdata):
        columndata, nbcols = string2vectors(testdata)
        
        for i in range(1, nbcols):
            plt.plot(columndata[0], columndata[i])
        plt.show()    

    def demo3(testdata):
        columndata, nbcols = string2vectors(testdata)
        s = pythonise_vector(columndata[0], "x")
        print(s)
        
        s = pythonise_vector(columndata[1], "y[i]")
        print(s)
        
        
    def demo4(testdata):
        s, names  = pythonise_text(testdata)
        print(s)
        exec(s)      

    def demo5(testdata):
        s = make_plotscript(testdata)
        print(s)
        exec(s)

     
    import matplotlib.pyplot as plt  
    demo5(testdata)
       
     
    
       
