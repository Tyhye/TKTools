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

photolist = []

class IVCanvas(tk.Canvas):
    
    def __init__(self, master=None, cnf={}, replay=False, scalestep=0.1, minscalerate=0.5, maxscalerate=5.0, **kw):
        super(IVCanvas, self).__init__(master=master, cnf=cnf, **kw)
        self.replay = replay
        self.scale_rate = 1.0
        self.scalestep=scalestep
        self.minscalerate = minscalerate
        self.maxscalerate = maxscalerate
        self.filepath = ""
        self.image = None
        self.photo_idx = -1
        self.bind("<Configure>", self._on_configure, add=True)
        self.bind("<Control-MouseWheel>", self._on_mouse_wheel, add=True)
        
    # def _resize_image_(self, image):
        
    
    def _fresh_canvas_(self):
        # resize image
        image_width, image_height = self.image.size
        canvas_height, canvas_width = self.winfo_height(), self.winfo_width()
        height = min(image_height, canvas_height)
        width = min(image_width, canvas_width)
        if (float(height)/image_height) < (float(width)/image_width):
            width = float(height) / image_height * image_width
        else: 
            height = float(width) / image_width * image_height
        width, height = int(self.scale_rate * width), int(self.scale_rate * height)
        
        # create image
        image = self.image.resize((width, height))
        
        # if self.photo_idx == -1:
        #     self.photo_idx = len(photolist)
        # else:
        #     photolist.pop(self.photo_idx)
        self.photo = ImageTk.PhotoImage(image=image)
        # photolist.append(self.photo)
        self.delete("image")
        self.image_id = super(IVCanvas, self).create_image(canvas_width/2, canvas_height/2, anchor='center', image=self.photo)
        self.update()

    def _on_configure(self, event):
        if self.image is None:
            pass
        else:
            self._fresh_canvas_()
            
    def _on_mouse_wheel(self, event):
        if event.delta > 0:
            self.scale_rate = min(self.scale_rate + self.scalestep, self.maxscalerate)
            self._fresh_canvas_()
        elif event.delta < 0:
            self.scale_rate = max(self.scale_rate - self.scalestep, self.minscalerate)
            self._fresh_canvas_()

        
    def set_replay(self, replay=True):
        self.replay = replay
        
    def create_image(self, imagename):
        # print(videoname)
        # print(self.filepath)
        self.scale_rate = 1.0
        if imagename == self.filepath:
            return
        self.filepath = imagename
        self.image = Image.open(self.filepath)
        self._fresh_canvas_()
        self.filepath = ""

    def create_video(self, videoname):
        self.scale_rate = 1.0
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
                self._fresh_canvas_()
                time.sleep(max(sleeptime-(time.time()-t1), 0))
                # print(videoname)
                # print(self.filepath)
                # input()
            elif self.replay:
                vc.set(cv2.CAP_PROP_POS_FRAMES, 0);
            else:
                self.filepath = ""
                break
                                

# if __name__ == '__main__':
#     window = tk.Tk()
#     canvas = IVCanvas(window)
#     canvas.pack(fill="both", expand=True)
#     def on_click():
#         canvas.create_image("D:/Devs/tktools/test.jpg")

#     btn = tk.Button(window, text="click", command=on_click)
#     btn.pack(side="top")
#     tk.mainloop()