# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
fileIO.py
-------------------------------------------------------------------------------
Aaron Robertson
General Use
Nov 2018
-------------------------------------------------------------------------------
File Description:
    Provides a basic GUI for file handling in python 2 and 3. 

Changelog:
11/08/18 - Modified from the original fileIO script.
-------------------------------------------------------------------------------
"""

#Libraries
#import numpy as np                                #Math
import os                                          #Input/Output
import sys                                         #Input/Output
if sys.version_info[0] < 3:
     IsPython3 = False
     from Tkinter import Tk,TclError               #Input/Output
     import tkFileDialog                           #Input/Output   
else:
     IsPython3 = True
     from tkinter import Tk,TclError,filedialog    #Input/Output


'''File Systems'''
'''-------------------------------------------------------------------------'''

def GetDir(initial_dir="./", default_dir="./", quiet = False):
    '''Opens a window that allows a user to select a directory.
       Returns the directory path.
    '''
    
    '''Opens a window that allows a user to select a directory, or provides
       one if none is specified.
       
       Inputs
       -------
       initial_dir : str
           The starting directory of the search. Selects the default
           directory of the script if no input is given.
       default_dir : str
           The absolute path to the default directory to return if no user 
           input is given.
       quiet : bool
           If true, the logging will be surpressed.
       
       Outputs
       -------
       dname : str
           The name of the selected directory.
    '''    
    
    #Set Window Attributes
    InitFileWindow()
    
    #Get Specified Directory
    if not quiet: print("Select a directory:")
    if IsPython3:
         dir_name = str((filedialog.askdirectory(initialdir=initial_dir,      \
                        title='Select Directory')) or default_dir)
    else:
         dir_name = str((tkFileDialog.askdirectory(initialdir=initial_dir,    \
                        title='Select Directory')) or default_dir) 
    dir_name = os.path.normpath(dir_name)
    if not quiet: print('%s\n' %dir_name)

    return dir_name

def GetFile(initial_dir="", default_file="", quiet = False):
    '''Opens a window that allows a user to select a specific file or selects
       a default file if no user input is given. A file extension filter can
       be applied to narrow results.
       
       Inputs
       -------
       initial_dir : str
           The starting directory for the file search. Defaults to the
           directory of the script if no input is given.
       default_file : str
           The path to the default file to return if no user input is given.
       filter  : dict
       
       quiet : bool
           If true, the logging will be surpressed.
       
       Outputs
       -------
       fname : str
           The name of the selected file.
    '''
    
    #Set Window Attributes
    InitFileWindow()
    
    #Get Specified File
    if not quiet: print("Select a file:")
    if IsPython3:
         fname = str((filedialog.askopenfilename(initialdir=initial_dir,      \
                      title = 'Select File', filetypes=[("CSV","*.csv"),      \
                      ("Text","*.txt")])) or default_file)
    else:
         fname = str((tkFileDialog.askopenfilename(initialdir=initial_dir,    \
                      title = 'Select File', filetypes=[("CSV","*.csv"),      \
                      ("Text","*.txt")])) or default_file)
         
    fname = os.path.normpath(fname)
    if not quiet: print("%s\n" %fname)

    return fname

def InitFileWindow():
    '''Called before GetFile() and GetDir() in order to hide hidden elements
       on UNIX systems. The user has the option to toggle file hidding.
    '''
    
    root = Tk()
    root.withdraw()

    ###########################################################################
    # Attempting to hide hidden elements in UNIX file systems
    # http://grokbase.com/t/python/tkinter-discuss/158pthm66v/tkinter-file-dialog-pattern-matching
    # http://wiki.tcl.tk/1060
    ###########################################################################
    try:
         # Call a dummy dialog with an impossible option to initialize the file
         # dialog without really getting a dialog window; this will throw a
         # TclError, so we need a try...except :
         try:
             root.tk.call('tk_getOpenFile', '-foobarbaz')
         except TclError:
             pass
         # Now, set the magic variables accordingly
         root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
         root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
    except:
         pass
    ###########################################################################    
        
    return root
    

'''File Loading/Saving'''
'''-------------------------------------------------------------------------'''

def LoadData(fname):
    '''
    Loads the results files for the indent profiler. The data is separated into
    a header, a global data block, and data blocks for the individual indents.
    
    Inputs
    ------
    fname : str
        The path to the file. The extension must be .txt or .csv to be loaded    
    
    Outputs
    -------
    header : class
        Header block data will be stored in a class for easy access.
    global : ndarray
        Global data is loaded into a [10xm] array. m = number of included indents.
        Formated in the form of,
            [Row]
            [IndentNumber]
            [Volume]
            [Pitch]
            [Width]
            [SideWallAreaL]
            [SideWallAreaR]
            [AvgDepth]
            [AvgSideAngleL]
            [AvgSideAngleR]
    indents :
        
    Notes
    -----
    A file extension check is provided in this function as a default. This 
    function will be used in multiple projects where file extensions are not
    guaranteed to be verfied prior to the LoadData() function call.
    '''

    #Set Extension
    filename, file_ext = os.path.splitext(fname)
    if (file_ext == '.txt'):
        delim = None
    elif (file_ext == '.csv'):
        delim = ','
    else:
        sys.exit("TERMINATE:LOAD_DATA:INVALID_EXTENSION")

    #Load Header
    header_length = 19
    header_index = np.arange(0, header_length)        #Header data rows
    with open(fname,'r') as fin:
        for i, line in enumerate(fin):
            if i in header_index:
                line_val = line.strip().split(delim)[-1]
                if i == 0: WireProfile      = str(line_val) 
                if i == 1: TotalSampleLength= float(line_val)    
                if i == 2: PtsPerRev        = int(line_val) 
                if i == 3: XSmoothing       = int(line_val)
                if i == 4: XMedian          = int(line_val)
                if i == 5: YAveraging       = int(line_val)
                if i == 6: YMedian          = int(line_val)
                if i == 7: DataState        = str(line_val)
                if i == 8: TimeStamp        = str(line_val)
                if i == 9: Rotation         = float(line_val)
                if i == 10: Twist           = float(line_val)
                if i == 11: TotalIndents    = int(line_val)
                if i == 12: XPtInterval     = float(line_val)
                if i == 13: YPtInterval     = float(line_val)
                if i == 14: AvgRadius       = float(line_val)      
                if i == 15: ExcludedIndents = str(line_val)
                if i == 16: 
                    Orientations = line.strip('\n').split(delim)[1:]
                    Orientations = [float(i) for i in Orientations]
                if i == 17:
                    AvgWidthPerRow = line.strip('\n').split(delim)[1:]
                    AvgWidthPerRow = [float(i) for i in AvgWidthPerRow]
                if i ==18:
                    IndentDistance = line.strip('\n').strip(';').split(delim)[1:]
                    IndentDistance = [float(i) for i in IndentDistance]
                
    header = HeaderInfo(WireProfile, TotalSampleLength, PtsPerRev, XSmoothing,   \
                        XMedian, YAveraging, YMedian, DataState, TimeStamp,      \
                        Rotation, Twist, TotalIndents, XPtInterval, YPtInterval, \
                        AvgRadius, ExcludedIndents, Orientations, AvgWidthPerRow,\
                        IndentDistance)

    #Load Global Data 
    header_length = 19
    header_index = np.arange(header_length, header_length+10)        #Header data rows
    global_block = np.array((0,0))
    with open(fname,'r') as fin:
        for i, line in enumerate(fin):
            if i in header_index:
                line_val = line.strip('\n').split(delim)[1:]
                line_val = [float(i) for i in line_val]
                line_val = np.asarray(line_val)
                if (i == header_length):
                    global_block = line_val
                else:
                    global_block = np.vstack((global_block,line_val))

    return header, global_block


class HeaderInfo():
    '''Used to store the header data of results files.'''
    
    def __init__(self, WireProfile, TotalSampleLength, PtsPerRev, XSmoothing,
				 XMedian, YAveraging, YMedian, DataState, TimeStamp, Rotation,
                 Twist, TotalIndents, XPtInterval, YPtInterval, AvgRadius,
                 ExcludedIndents, Orientations, AvgWidthPerRow, IndentDistance):
        self.WireProfile = WireProfile
        self.TotalSampleLength = TotalSampleLength
        self.PtsPerRev = PtsPerRev
        self.XSmoothing = XSmoothing
        self.XMedian = XMedian
        self.YAveraging = YAveraging
        self.YMedian = YMedian
        self.DataState = DataState
        self.TimeStamp = TimeStamp
        self.Rotation = Rotation    
        self.Twist = Twist
        self.TotalIndents = TotalIndents
        self.TimeStamp = TimeStamp
        self.XPtInterval = XPtInterval
        self.YPtInterval = YPtInterval
        self.AvgRadius = AvgRadius
        self.ExcludedIndents = ExcludedIndents
        self.Orientations = Orientations
        self.AvgWidthPerRow = AvgWidthPerRow
        self.IndentDistance = IndentDistance


if __name__ == "__main__":
    '''python fileIO.py
       Running this command will execute the test suite.
    '''   


    file_temp = GetFile()
    dir_temp = GetDir()
    
    #root.mainloop()