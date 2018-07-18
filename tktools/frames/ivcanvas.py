#!/usr/bin/env python 
# -*- code:utf-8 -*- 
'''
 @Author: tyhye.wang 
 @Date: 2018-07-17 21:09:05 
 @Last Modified by:   tyhye.wang 
 @Last Modified time: 2018-07-17 21:09:05 
'''

import tkinter as tk
from PIL import Image, ImageTk
import cv2
import threading
import time

class IVCanvas(tk.Canvas):
    
    def __init__(self, master=None, cnf={}, replay=False, **kw):
        super(IVCanvas, self).__init__(master=master, cnf=cnf, **kw)
        self.replay = replay
        self.filepath = ""
        self.image = None
        # self.bind("<Configure>", self._on_configure, add=True)
        
    def _resize_image_(self, image):
        image_width, image_height = image.size
        canvas_height, canvas_width = self.winfo_height(), self.winfo_width()
        height = min(image_height, canvas_height)
        width = min(image_width, canvas_width)
        if (float(height)/image_height) < (float(width)/image_width):
            width = int(float(height) / image_height * image_width)
        else: 
            height = int(float(width) / image_width * image_height)
        return image.resize((width, height))
    
    def _on_configure(self, event):
        if self.image is None:
            pass
        else:
            image = self._resize_image_(self.image)
            global photo
            photo = ImageTk.PhotoImage(image=image)
            self.delete("image")
            self.image_id = super(IVCanvas, self).create_image(self.winfo_width()/2, self.winfo_height()/2, anchor='center', image=photo)
            self.update()

    def set_replay(self, replay=True):
        self.replay = replay
        
    def create_image(self, imagename):
        # print(videoname)
        # print(self.filepath)
        if imagename == self.filepath:
            return
        self.filepath = imagename
        self.image = Image.open(self.filepath)
        image = self._resize_image_(self.image)
        global photo
        photo = ImageTk.PhotoImage(image=image)
        self.delete("image")
        self.image_id = super(IVCanvas, self).create_image(self.winfo_width()/2, self.winfo_height()/2, anchor='center', image=photo)
        self.update()
        self.filepath = ""

    def create_video(self, videoname):
        if videoname == self.filepath:
            return
        self.filepath = videoname
        vc = cv2.VideoCapture(self.filepath)
        while self.filepath == videoname:
            t1 = time.time()
            sleeptime = 1.0 / vc.get(cv2.CAP_PROP_FPS)
            ret, frame = vc.read()
            if ret:
                width, height = self.winfo_width(), self.winfo_height()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                self.image = Image.fromarray(frame)
                image = self._resize_image_(self.image)
                global photo
                photo = ImageTk.PhotoImage(image=image)
                self.delete("image")
                self.image = super(IVCanvas, self).create_image(self.winfo_width()/2, self.winfo_height()/2, anchor='center', image=photo)
                self.update()
                time.sleep(max(sleeptime-(time.time()-t1), 0))
            elif self.replay:
                vc.set(cv2.CAP_PROP_POS_FRAMES, 0);
            else:
                break
        self.filepath = ""

# if __name__ == '__main__':
#     window = tk.Tk()
#     canvas = IVCanvas(window)
#     canvas.pack(fill="both", expand=True)
#     def on_click():
#         canvas.create_image("D:/Devs/tktools/test.jpg")

#     btn = tk.Button(window, text="click", command=on_click)
#     btn.pack(side="top")
#     tk.mainloop()