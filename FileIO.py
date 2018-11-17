# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
AMP-AmlorisMiscPython: FileIO.py
-------------------------------------------------------------------------------
Aaron Robertson
General Use
Nov 2018
-------------------------------------------------------------------------------
File Description:
    Provides a basic GUI for file handling in python 2 and 3. 

Changelog:
11/08/18 - Modified from the original fileIO script.
11/09/18 - Removed specialized file loading functions. Added filtering to GetFile()
11/09/18 - Added CLI prompts and window naming for GetFile() and GetDir()
11/16/18 - Added GetFiles(). Returns an iterable list of selected files.
-------------------------------------------------------------------------------
"""

#Libraries
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

def GetDir(initial_dir="./", default_dir="./", cli_prompt="Select a directory:", 
           window_name='Select Directory', quiet = False):    
    '''Opens a window that allows a user to select a directory.
       Returns the directory path.
       
       Inputs
       -------
       initial_dir : str (optional)
           The starting directory of the search. Selects the default
           directory of the script if no input is given.
       default_dir : str (optional)
           The absolute path to the default directory to return if no user 
           input is given.
       cli_prompt: str (optional)
           The command line interface prompt for directory selection.
       window_name : str (optional)
           Name of the GUI window.
       quiet : bool (optional)
           If true, the logging will be surpressed.
       
       Outputs
       -------
       dname : str
           The path of the selected directory.
    '''    
    
    #Set Window Attributes
    InitFileWindow()
    
    #Get Specified Directory
    if not quiet: print(cli_prompt)
    if IsPython3:
         dir_name = str((filedialog.askdirectory(initialdir=initial_dir,      \
                        title=window_name)) or default_dir)
    else:
         dir_name = str((tkFileDialog.askdirectory(initialdir=initial_dir,    \
                        title=window_name)) or default_dir) 
    dir_name = os.path.normpath(dir_name)
    if not quiet: print('%s\n' %dir_name)

    return dir_name

def GetFile(initial_dir="", default_file="", filters=[("CSV","*.csv"), ("Text","*.txt")],
            cli_prompt="Select a file:", window_name='Select File', quiet = False):
    '''Opens a window that allows a user to select a file.
       Filters can be applied to narrow results.
       Returns the file path.
       
       Inputs
       -------
       initial_dir : str (optional)
           The starting directory for the file search. Defaults to the
           directory of the script if no input is given.
       default_file : str (optional)
           The path to the default file to return if no user input is given. This
           function will fail if a user does not select a file and no default file
           is given.
       filter  : list of tuples (optional)
           A file filter composed of strings in a dict. Valid input is show below
               [("CSV","*.csv"), ("Text","*.txt")]
           If no argument is specified only .txt and .csv files will be shown.
       cli_prompt: str (optional)
           The command line interface prompt for file selection.
       window_name : str (optional)
           Name of the GUI window.
       quiet : bool (optional)
           If true, the logging will be surpressed.
       
       Outputs
       -------
       fname : str
           The path of the selected file.
    '''
    
    #Set Window Attributes
    InitFileWindow()
    
    #Get Specified File
    if not quiet: print(cli_prompt)
    if IsPython3:
         fname = str((filedialog.askopenfilename(initialdir=initial_dir,          \
                      title = window_name, filetypes=filters)) or default_file)
    else:
         fname = str((tkFileDialog.askopenfilename(initialdir=initial_dir,        \
                      title = window_name, filetypes=filters)) or default_file)
         
    fname = os.path.normpath(fname)
    if not quiet: print("%s\n" %fname)

    return fname

def GetFiles(initial_dir="", filters=[("CSV","*.csv"), ("Text","*.txt")],
            cli_prompt="Select a file:", window_name='Select File', quiet = False):
    '''Opens a window that allows a user to select multiple files.
       Filters can be applied to narrow results.
       Returns an iterable list of selected files.
       
       Inputs
       -------
       initial_dir : str (optional)
           The starting directory for the file search. Defaults to the
           directory of the script if no input is given.
       filter  : list of tuples (optional)
           A file filter composed of strings in a dict. Valid input is show below
               [("CSV","*.csv"), ("Text","*.txt")]
           If no argument is specified only .txt and .csv files will be shown.
       cli_prompt: str (optional)
           The command line interface prompt for file selection.
       window_name : str (optional)
           Name of the GUI window.
       quiet : bool (optional)
           If true, the logging will be surpressed.
       
       Outputs
       -------
       fname : iterable list
           A list of strings to the path of the selected files.
    '''
    
    #Set Window Attributes
    InitFileWindow()
    
    #Get Specified File
    if not quiet: print(cli_prompt)
    if IsPython3:
         fname = filedialog.askopenfilenames(initialdir=initial_dir,          \
                      title = window_name, filetypes=filters)
    else:
         fname = tkFileDialog.askopenfilenames(initialdir=initial_dir,        \
                      title = window_name, filetypes=filters)
         
    #fname = os.path.normpath(fname)
    if not quiet:
        for i in fname:
            print(i)
        print("")

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


if __name__ == "__main__":
    '''python fileIO.py
       Running this command will execute the test suite.
    '''   

    file_temp = GetFile()
    files_temp = GetFiles()
    dir_temp = GetDir()