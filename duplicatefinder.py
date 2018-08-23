#!/usr/bin/env python 
# -*- code:utf-8 -*- 
'''
 @Author: tyhye.wang 
 @Date: 2018-08-23 10:25:10 
 @Last Modified by:   tyhye.wang 
 @Last Modified time: 2018-08-23 10:25:10 
'''

import tkinter as tk
from tktools.tools.duplicatefinder import Duplicate

def main():
    
    window = tk.Tk()
    window.geometry("960x540")
    cl = Duplicate(window)
    window.mainloop()
    
if __name__ == "__main__":
    main()