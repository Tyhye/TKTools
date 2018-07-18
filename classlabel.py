#!/usr/bin/env python 
# -*- code:utf-8 -*- 
'''
 @Author: tyhye.wang 
 @Date: 2018-07-05 13:43:02 
 @Last Modified by:   tyhye.wang 
 @Last Modified time: 2018-07-18 14:39:44 
'''

import tkinter as tk
from tktools.tools.classlabel import ClassLabel

def main():
    
    window = tk.Tk()
    window.geometry("960x540")
    cl = ClassLabel(window)
    window.mainloop()
    
if __name__ == "__main__":
    main()