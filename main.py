'''
 * @Author: tyhye.wang 
 * @Date: 2018-07-05 13:43:02 
 * @Last Modified by:   tyhye.wang 
 * @Last Modified time: 2018-07-05 13:43:02 
'''
# -*- code:utf-8 -*-



import tkinter as tk
from imagelabel import ImageLabel
# from videolabel import VideoLabel
# from duplicate import Duplicate

def main():
    
    window = tk.Tk()
    window.geometry("960x540")
    # l = tk.Label(window, text="Hello World!")
    # l.pack()
    # vdl = VideoLabel(window)
    cl = ImageLabel(window)
    # dp =  Duplicate(window)
    window.mainloop()
    
if __name__ == "__main__":
    main()