# -*- coding:utf-8 -*-
'''
 * @Author: tyhye.wang 
 * @Date: 2018-07-11 18:56:21 
 * @Last Modified by:   tyhye.wang 
 * @Last Modified time: 2018-07-11 18:56:21 
'''

import tkinter as tk
from PIL import Image
from PIL import ImageTk
from skimage import transform
import tkinter.filedialog as tkFiledialog
import tkinter.messagebox as tkMessageBox
import os
import shutil

from ...filecheck import is_image_file
from ...frames.multicolumnlistbox import MultiListbox
from .duplicate_helper import Similarity_Computer #, ComputeThread

Image_Classes = ["优质", "良好", "一般", "劣质"]

class Duplicate(object):
    min_width = 40
    min_height = 40
    
    def __init__(self, master=None):
        if master is None:
            self.father = tk.Tk(master)
        else:
            self.father = master
        self.father.title("Duplicate Finder")
        # self.compute_thread = None
        self.Computer = Similarity_Computer()
        # ----------------------------
        # left frame for loading files and list
        # 最右边的部分
        # ----------------------------
        self.f_loading_file_frame = tk.Frame(self.father, borderwidth=5)
        self.f_loading_file_frame.pack(side="top", fill="x")

        self.image_dir = ""
        self.image_dir_var = tk.StringVar()
        self.e_image_dir_entry = tk.Entry(master=self.f_loading_file_frame, textvariable=self.image_dir_var)
        self.e_image_dir_entry.pack(side="left", fill='x', expand=True)
        self.b_image_dir_select_button = tk.Button(master=self.f_loading_file_frame, text="select dir", command=self.on_select_dir)
        self.b_image_dir_select_button.pack(side="left")
        self.b_image_dir_load_button = tk.Button(master=self.f_loading_file_frame, text="loading images", command=self.on_load_dir)
        self.b_image_dir_load_button.pack(side="left")
        
        self.log_var = tk.StringVar()
        self.log_var.set("Duplicate Finder and Remover! v.0.1.0")
        self.l_log_message_label = tk.Label(master=self.father, textvariable=self.log_var, anchor='w')
        self.l_log_message_label.pack(side="bottom", fill="x")

        # ----------------------------
        # right frame for classes and prev and next
        # 最右边的部分
        # ----------------------------
        self.f_operate_father_frame = tk.Frame(self.father, borderwidth=5)
        self.f_operate_father_frame.pack(side="right", anchor="n")
        self.f_operate_frame = tk.Frame(self.f_operate_father_frame, borderwidth=2, relief="ridge")
        self.f_operate_frame.pack(fill="both", expand=True)
        self.f_threshold_frame = tk.Frame(self.f_operate_frame, borderwidth=2)
        self.f_threshold_frame.pack(side="top", fill="x")
        self.l_threshold = tk.Label(self.f_threshold_frame, text="Threshold:")
        self.l_threshold.pack(side="left")
        self.threshold = 0.8
        self.threshold_var = tk.StringVar(value=self.threshold)
        self.e_threshold_entry = tk.Entry(self.f_threshold_frame, textvariable=self.threshold_var, width=12)
        self.e_threshold_entry.pack(side="right")
        self.compute_cancel_var = tk.StringVar()
        self.compute_cancel_var.set("compute similarity")
        self.b_compute_similiar_button = tk.Button(master=self.f_operate_frame, textvariable=self.compute_cancel_var, command=self.on_compute_similarity)
        self.b_compute_similiar_button.pack(side="top", fill="x")
        self.b_delete_selection_button = tk.Button(master=self.f_operate_frame, text="delete selected", command=self.on_delete_selected)
        self.b_delete_selection_button.pack(side="top", fill="x")
        self.b_delete_all_button = tk.Button(master=self.f_operate_frame, text="delete all", command=self.on_delete_all)
        self.b_delete_all_button.pack(side="top", fill="x")
        
        # ----------------------------
        # content frame for classes and prev and next
        # 中间部分
        # ----------------------------
        self.f_contant_frame = tk.Frame(self.father, borderwidth=5)
        self.f_contant_frame.pack(fill="both", expand=True)
        # list frame 
        self.f_list_frame = tk.Frame(self.f_contant_frame, borderwidth=5)
        self.f_list_frame.pack(side="top", fill="both", expand=True)
        self.select_image_pair = (None, None)
        self.imagefiles = []
        duplicate_titles = [("query",20), ("searched",20), ("score",10)]
        self.ml_duplicates_listbox = MultiListbox(
            self.f_list_frame, lists=duplicate_titles, height=1, selectmode="browse")
        self.ml_duplicates_listbox.pack(fill="both", expand=True)
        self.ml_duplicates_listbox.bind("<Button-1>", self.on_ml_button1, True)
        self.ml_duplicates_listbox.bind("<Control-1>", self.on_ml_button1, True)

        self.canvas_frame = tk.Frame(self.f_contant_frame, borderwidth=5, height=128)
        self.canvas_frame.pack(side="bottom", fill="both")
        self.canvas1 = tk.Canvas(self.canvas_frame, relief="ridge", borderwidth=5,width=1)
        self.canvas1.pack(side="left", fill="both",expand=True)
        self.canvas2 = tk.Canvas(self.canvas_frame, relief="ridge", borderwidth=5,width=1)
        self.canvas2.pack(side="right", fill="both",expand=True)

    

    def on_compute_similarity(self):
        # if self.compute_thread is not None:
        #     if self.compute_thread.is_alive():
        #         self.compute_thread = None
        #     else:
        #         self.compute_thread.stop()
        if self.Computer.running:
            self.Computer.running = False
            self.log_var.set("Summary: %d duplicate image pair founded"%self.ml_duplicates_listbox.size())
            self.compute_cancel_var.set("compute similarity")
            self.b_compute_similiar_button.update()
        else:
            self.threshold = float(self.e_threshold_entry.get())
            if self.has_been_deleted:
                self.on_load_dir()
            self.ml_duplicates_listbox.delete(0, tk.END)
            self.compute_cancel_var.set("cancel computing")
            self.b_compute_similiar_button.update()
            # self.compute_thread = ComputeThread(1, "computing similarity", self.imagefiles, image_dir=self.image_dir, threshold=self.threshold, listbox=self.ml_duplicates_listbox, logvar=self.log_var, log_label=self.l_log_message_label)
            # self.compute_thread.start()
            self.Computer.compute(self.imagefiles, image_dir=self.image_dir, threshold=self.threshold, listbox=self.ml_duplicates_listbox, logvar=self.log_var, log_label=self.l_log_message_label)
            self.log_var.set("Summary: %d duplicate image pair founded"%self.ml_duplicates_listbox.size())
            self.compute_cancel_var.set("compute similarity")
            self.b_compute_similiar_button.update()
            # self.l_log_message_label.update()

    def on_delete_selected(self):
        selected_indexs = self.ml_duplicates_listbox.curselection()
        pairs = self.ml_duplicates_listbox.get(0, last=tk.END)
        path_index_pairs = [(idx, pairs[1][idx]) for idx in selected_indexs]
        path_index_pairs.sort(key=lambda x : x[0], reverse=True)
        record_paths = []
        print("delete searched")
        for idx, (index, filepath) in enumerate(path_index_pairs):
            path = os.path.join(os.path.normcase(self.image_dir), os.path.normcase(filepath))
            if os.path.exists(path):
                os.remove(path)
            self.ml_duplicates_listbox.delete(index)
            self.log_var.set("%d / %d has been deleted!"%(idx+1, len(path_index_pairs)))
            self.l_log_message_label.update()
            record_paths.append(filepath)
        pairs = self.ml_duplicates_listbox.get(0, last=tk.END)
        querypaths, searchedpaths = pairs[0], pairs[1]
        indexs = []
        for idx, querypath, searchedpath in enumerate(zip(querypaths, searchedpaths)):
            if querypath in record_paths or searchedpath in record_paths:
                indexs.append(idx)
            self.log_var.set("%d / %d has been checked!"%(idx+1, len(querypaths)))
            self.l_log_message_label.update()
        indexs.sort(reverse=True)
        print("delete query")
        for idx, index in enumerate(indexs):
            self.ml_duplicates_listbox.delete(index)
            self.log_var.set("%d / %d has been deleted!"%(idx+1, len(indexs)))
            self.l_log_message_label.update()
            
        self.select_image_pair = None
        self.fresh_canvas()
        self.has_been_deleted = True
        
    def on_delete_all(self):
        pairs = self.ml_duplicates_listbox.get(0, last=tk.END)
        needdeletes = pairs[1]
        for idx, filepath in enumerate(needdeletes):
            path = os.path.join(os.path.normcase(self.image_dir), os.path.normcase(filepath))
            if os.path.exists(path):
                os.remove(path)
            self.log_var.set("%d / %d have been deleted!"%(idx+1, len(needdeletes)))
            self.l_log_message_label.update()
            self.ml_duplicates_listbox.delete(0)
        self.select_image_pair = None
        self.fresh_canvas()
        self.has_been_deleted = True
    
    def on_select_dir(self):
        selected_dir = tkFiledialog.askdirectory()
        if selected_dir == "":
            return
        else:
            self.image_dir_var.set(os.path.normcase(selected_dir))
            self.e_image_dir_entry.focus_set()
            self.e_image_dir_entry.select_range(0, len(selected_dir))
            self.e_image_dir_entry.icursor(len(selected_dir))
            self.e_image_dir_entry.xview_moveto(len(selected_dir))

    def on_load_dir(self):
        image_dir = self.e_image_dir_entry.get()
        if not os.path.exists(image_dir):
            tkMessageBox.showwarning(title="wrong dir", message="\"%s\" is not found!, please check again!"%(image_dir))
            return
        self.image_dir = image_dir
        self.imagefiles.clear()
        # tkMessageBox.showinfo(title="Loading", message="Loading image list of \"%s\""%(image_dir))
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                if not is_image_file(file):
                    continue
                imagepath = os.path.join(root[len(image_dir)+1:], file)
                self.imagefiles.append(imagepath)
                self.log_var.set("Searching: %d images searched!"%(len(self.imagefiles)))
                self.l_log_message_label.update()
        self.log_var.set("Summary: %d images"%(len(self.imagefiles)))
        self.l_log_message_label.update()
        self.has_been_deleted = False

    def on_ml_button1(self, event):
        if self.ml_duplicates_listbox.size() > 0:
            row = self.ml_duplicates_listbox.nearest(event.y)
            pair = self.ml_duplicates_listbox.get(row)
            self.select_image_pair = (pair[0], pair[1])
            self.fresh_canvas()

    def _load_image_(self, imagepath, canvas):
        imagepath = os.path.join(os.path.normcase(self.image_dir), os.path.normcase(imagepath))
        image = Image.open(imagepath)
        image_width, image_height = image.size
        canvas_height, canvas_width = canvas.winfo_height(), canvas.winfo_width()
        height = min(max(self.min_height, image_height), canvas_height)
        width = min(max(self.min_width, image_width), canvas_width)
        if (float(height)/image_height) < (float(width)/image_width):
            width = int(float(height) / image_height * image_width)
        else: 
            height = int(float(width) / image_width * image_height)
        return image.resize((width, height))

    def fresh_canvas(self):
        self.canvas1.delete("image")
        self.canvas2.delete("image")
        if self.select_image_pair is not None:
            path1, path2 = self.select_image_pair
            image1, image2 = self._load_image_(path1, self.canvas1), self._load_image_(path2, self.canvas2), 
            global photo1, photo2
            photo1 = ImageTk.PhotoImage(image1)
            photo2 = ImageTk.PhotoImage(image2)
            # self.canvas.create_image(0,0,anchor='nw', image=photo)
            self.image1 = self.canvas1.create_image(self.canvas1.winfo_width()/2, self.canvas1.winfo_height()/2, anchor='center', image=photo1)
            self.image2 = self.canvas2.create_image(self.canvas2.winfo_width()/2, self.canvas2.winfo_height()/2, anchor='center', image=photo2)

