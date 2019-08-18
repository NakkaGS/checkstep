#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.24.1
#  in conjunction with Tcl version 8.6
#    Aug 16, 2019 11:38:10 AM CDT  platform: Windows NT

import sys
from tkinter import filedialog
from tkinter import *

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global awlpath #Label pathAWLFile
    awlpath = StringVar()

    global prog_var
    prog_var = tk.IntVar()

    global checkCo #CheckBotton Comments
    checkCo = tk.IntVar()

    global checkFB #CheckBotton Network
    checkFB = tk.IntVar()

    global finishTask
    finishTask = tk.StringVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
    awlpath.set("AWL Path: ")

def destroy_window():   
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import checkStep
    checkStep.vp_start_gui()

#Function to open browse and select awl file
def awlBrowse():
    root = Tk() #withdraw() unable open extra window
    root.file = filedialog.askopenfilename(initialdir = "/",title = "Select AWL",filetypes = (("AWL file","*.awl"),("All files","*.*")))
    awlpath.set(root.file)

#Function to do the logic when Start is selected
def startProgram():
    if checkCo.get() == True:
      comments(awlpath.get())
    if checkFB.get() == True:
      network(awlpath.get())
    finishTask.set("Done")
    
#Function to check if there is a network if comment
def comments(awlfilepath):
   FB = ""
   same = ""

   awl_com = open("generated/comments_awl.txt", "w") 

   #string to compare if awl
   stringToMatch = 'FUNCTION_BLOCK FB '
   comment = "" #If is necessary to check if the network has a comments, change to ''

   #initialize variables
   num_lines = 0
   count = 0
   count = len(open(awlfilepath).readlines())


   
   #Open generated txt
   with open(awlfilepath, 'r') as file:

       for line in file:

        #for progress bar... in process
        num_lines += 1
        progress = count/num_lines
        update(progress)

        #There is a lengh difference when the decimal changes
        if stringToMatch in line:

            if len(line) == 23:
               FB = line[18:22]
            if len(line) == 22:
               FB = line[18:21]
            if len(line) == 21:
               FB = line[18:20]
                   
        #Change from STR to Int
        if FB == "":
            FB = 0
            same = FB
            
        #Rules
        #We don't need to check FB 0-100 and 1600-1800
            
        #Safety FBs or Basic FBs
        if 1600 < int(str(FB)) < 1800 or 0 < int(str(FB)) < 200:
            FB = 0
            same = 0
            
        #Logic   
        if comment in line:
            if same != FB and FB != 0: #to make sure that will appear just once the FB
               #print(FB)
               same = FB
               awl_com.write("FB " + FB + "\n")
   
   #Close generated txt
   awl_com.close()

   print("Checking if Network has Comments...DONE!\n")
    
#Function to check if the network has the same name as the FG Name *needs to implement Symbol names
def network(awlfilepath):

   #initialize variables
   FB = ""
   same = ""
   mesmo = ""

   FBName = ''
   
   #string to compare if awl
   stringToMatch = 'FUNCTION_BLOCK FB '
   title = 'TITLE ='
   
   #Open generated txt
   awl_net = open("generated/network_awl.txt", "w")
   
   with open(awlfilepath, 'r') as file:
       
      for line in file:

        #There is a lengh difference when the decimal changes
        if stringToMatch in line:      
            if len(line) == 23:
               FB = line[18:22]
            if len(line) == 22:
               FB = line[18:21]
            if len(line) == 21:
               FB = line[18:20]
               
        #Change from STR to Int
        if FB == "":
            FB = 0
            same = FB
            
        #Rules
        #We don't need to check FB 0-100 and 1600-1800
            
        #Safety FBs or Basic FBs
        if 1600 < int(str(FB)) < 1800 or 0 < int(str(FB)) < 200:
            FB = 0
            same = 0

        #Logic    
        if title in line:
            if same != FB and FB != 0: #to make sure that will appear just once the FB
               FBName = line[7:16] #copy FB name from the network
               same = FB

            if same == FB and mesmo != FB and FB != 0:
               if line[7:16] != FBName: #to make sure that will appear just once the FB
                  #print("FB "+FB)
                  awl_net.write("FB " + str(FB) + "\n")
                  mesmo = FB
   
   #Close generated txt
   awl_net.close()
   
   print("Checking if Network matchs with FB Name...DONE!\n")

#Function to update the progress bar *NOT WORKING
def update (v):
    #print ('Progress_Bar: update: v =', v)    
    prog_var.set(int(v*100))