#!/usr/bin/env python 
# -*- code:utf-8 -*- 
'''
 @Author: tyhye.wang 
 @Date: 2018-07-17 21:11:35 
 @Last Modified by:   tyhye.wang 
 @Last Modified time: 2018-07-17 21:11:35 
'''
import os

import tkinter as tk
from ..frames.ivcanvas import IVCanvas

Classes = [
("000" , "000"), 
("001" , "001"), 
("002" , "002"), 
("003" , "003"), 
("004" , "004"), 
("005" , "005")] 

_version_ = "v.0.1.2"

class ClassLabel(object):
    min_width = 48
    min_height = 48
    
    def __init__(self, master=None):
        if master is None:
            self.father = tk.Tk(master)
        else:
            self.father = master
        self.father.title("Class Label")
        
        # ----------------------------
        # left frame for loading files and list
        # ----------------------------
        self.f_loading_file_frame = tk.Frame(self.father, borderwidth=5)
        self.f_loading_file_frame.pack(side="left", fill="y")
        
        self.f_loading_file_top_frame = tk.Frame(self.f_loading_file_frame)
        self.f_loading_file_top_frame.pack(side="top", fill="x")

        self.image_dir = ""
        self.image_dir_var = tk.StringVar()
        self.e_image_dir_entry = tk.Entry(master=self.f_loading_file_top_frame, width=20, textvariable=self.image_dir_var)
        self.e_image_dir_entry.pack(side="left")
        self.b_image_dir_select_button = tk.Button(master=self.f_loading_file_top_frame, text="select dir", command=self.on_select_dir)
        self.b_image_dir_select_button.pack(side="left", after=self.e_image_dir_entry)
        self.b_image_dir_load_button = tk.Button(master=self.f_loading_file_top_frame, text="loading files", command=self.on_load_dir)
        self.b_image_dir_load_button.pack(side="left", after=self.b_image_dir_select_button)
        
        self.now_index = 0
        self.imagefiles = []
        self.image_files_var = tk.StringVar()
        self.image_files_var.set(self.imagefiles)
        self.f_loading_file_list_frame = tk.Frame(self.f_loading_file_frame)
        self.f_loading_file_list_frame.pack(fill="both", expand=True)
        
        self.sc_imagefiles_scorllbar = tk.Scrollbar(self.f_loading_file_list_frame)
        self.sc_imagefiles_scorllbar.pack(side="right", fill="y")
        self.ls_imagefiles_listbox = tk.Listbox(self.f_loading_file_list_frame, borderwidth=3, listvariable=self.image_files_var, relief='groove', selectmode="browse", yscrollcommand=self.sc_imagefiles_scorllbar.set)
        self.ls_imagefiles_listbox.bind("<ButtonRelease-1>", self.on_select_imgitem)
        self.ls_imagefiles_listbox.pack(side="left", fill="both", expand=True)
        self.sc_imagefiles_scorllbar.config(command=self.ls_imagefiles_listbox.yview)

        self.log_var = tk.StringVar()
        self.log_var.set("multi image label tool! %s"%(_version_))
        self.l_log_message_label = tk.Label(master=self.f_loading_file_frame, textvariable=self.log_var, anchor='w')
        self.l_log_message_label.pack(side="bottom", fill="x")

        # ----------------------------
        # right frame for classes and prev and next
        # ----------------------------
        self.f_label_operate_frame = tk.Frame(self.father, borderwidth=5)
        self.f_label_operate_frame.pack(side="right", fill="y")
        self.b_prev_button = tk.Button(master=self.f_label_operate_frame, text="prev", width=20, command=self.on_prev)
        self.b_prev_button.pack(side="top", fill='x')
        
        self.f_label_operate_ratio_frame = tk.Frame(self.f_label_operate_frame)
        self.f_label_operate_ratio_frame.pack(fill="y", anchor="w")
        self.label_ratio_var = tk.StringVar()
        self.label_ratio_list = []
        for idx, (class_name, class_value) in enumerate(Classes):
            tmp_ratio_button = tk.Radiobutton(self.f_label_operate_ratio_frame, text=class_name, variable=self.label_ratio_var, value=class_value, command=self.on_next)
            tmp_ratio_button.pack(side="top", anchor="w")
            self.label_ratio_list.append(tmp_ratio_button)
        self.label_ratio_var.set(Classes[0][1])
        self.b_next_button = tk.Button(master=self.f_label_operate_frame, text="next", command=self.on_next)
        self.b_next_button.pack(side="top", fill='x')
        self.b_extract_button = tk.Button(master=self.f_label_operate_frame, text="extract_files", command=self.on_extract)
        self.b_extract_button.pack(side="top", fill='x')

        # ----------------------------
        # center frame for canvas
        # ----------------------------
        self.canvas_frame = tk.Frame(self.father, borderwidth=5)
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas = IVCanvas(self.canvas_frame, relief="ridge", borderwidth=5)
        self.canvas.pack(fill="both", expand=True)
        self.file_path_var = tk.StringVar()
        self.file_path_var.set("waiting for image")
        self.l_file_path_label = tk.Label(master=self.canvas_frame, textvariable=self.file_path_var)
        self.l_file_path_label.pack(side="bottom", fill='x')

    def on_prev(self):
        pass
    
    def on_next(self):
        pass
    
    def on_select_imgitem(self, event):
        pass

    def on_select_dir(self):
        pass

    def on_load_dir(self):
        pass

    def fresh_ratio(self):
        pass

    def fresh_canvas(self): 
        pass
        
    def label_for_this_image(self):
        pass
    
    def on_extract(self):
        pass


# if __name__ == '__main__':
#     window = tk.Tk()
#     cl = ClassLabel(window)
#     tk.mainloop()
