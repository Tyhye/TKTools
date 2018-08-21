#!/usr/bin/env python
# -*- code:utf-8 -*-
'''
 @Author: tyhye.wang 
 @Date: 2018-07-17 21:11:35 
 @Last Modified by:   tyhye.wang 
 @Last Modified time: 2018-07-17 21:11:35 
'''
import os
import shutil
import datetime

import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox

from ...frames.ivcanvas import IVCanvas
from ...filecheck import is_image_file, is_video_file
from .classconfig import askClassesDialog

Classes = [
    ("000", "0"),
    ("001", "1"),
    ("002", "2"),
    ("003", "3"),
    ("004", "4"),
    ("005", "5")]

Pre_Define_Color = {
    "unlabeled": "white",
    "labeled": "darkseagreen"
}

_version_ = "v.0.1.2"


class ClassLabel(object):
    min_width = 48
    min_height = 48
    '''
    params:
      filetype: "both","image","video", `image` or `video` or `both` files are 
      used for label
    '''

    def __init__(self, master=None):
        if master is None:
            self.father = tk.Tk()
        else:
            self.father = master
        self.father.title("Class Label")
        self._load_config_()
        self.father.geometry(self.config["shape"])
        self.father.bind("<Configure>", self._on_resize_, add=True)

        # ----------------------------
        # left frame for loading files and list
        # ----------------------------
        self.f_loading_file_frame = tk.Frame(self.father, borderwidth=5)
        self.f_loading_file_frame.pack(side="left", fill="y")

        self.f_loading_file_top_frame = tk.Frame(self.f_loading_file_frame)
        self.f_loading_file_top_frame.pack(side="top", fill="x")

        self.image_dir = ""
        self.image_dir_var = tk.StringVar()
        self.e_image_dir_entry = tk.Entry(
            master=self.f_loading_file_top_frame, width=20, textvariable=self.image_dir_var)
        self.e_image_dir_entry.pack(side="left")
        self.b_image_dir_select_button = tk.Button(
            master=self.f_loading_file_top_frame, text="select dir", command=self.on_select_dir)
        self.b_image_dir_select_button.pack(
            side="left", after=self.e_image_dir_entry)
        self.b_image_dir_load_button = tk.Button(
            master=self.f_loading_file_top_frame, text="loading files", command=self.on_load_dir)
        self.b_image_dir_load_button.pack(
            side="left", after=self.b_image_dir_select_button)

        self.f_label_legend_frame = tk.Frame(self.f_loading_file_frame, borderwidth=5)
        self.f_label_legend_frame.pack(side="top", fill="x")
        self.l_labeled_legend_label = tk.Label(self.f_label_legend_frame, text="labeled", bg=Pre_Define_Color["labeled"], borderwidth=1, relief='solid')
        self.l_labeled_legend_label.pack(side="left",fill="x",expand=True)
        self.l_unlabeled_legend_label = tk.Label(self.f_label_legend_frame, text="unlabeled", bg=Pre_Define_Color["unlabeled"], borderwidth=1, relief='solid')
        self.l_unlabeled_legend_label.pack(side="right",fill="x",expand=True)

        self.now_index = 0
        self.imagefiles = []
        self.image_files_var = tk.StringVar()
        self.image_files_var.set(self.imagefiles)
        self.f_loading_file_list_frame = tk.Frame(self.f_loading_file_frame)
        self.f_loading_file_list_frame.pack(fill="both", expand=True)

        self.sc_imagefiles_scorllbar = tk.Scrollbar(
            self.f_loading_file_list_frame)
        self.sc_imagefiles_scorllbar.pack(side="right", fill="y")
        self.ls_imagefiles_listbox = tk.Listbox(self.f_loading_file_list_frame, borderwidth=3, listvariable=self.image_files_var,
                                                relief='groove', selectmode="browse", yscrollcommand=self.sc_imagefiles_scorllbar.set)
        self.ls_imagefiles_listbox.bind(
            "<ButtonRelease-1>", self.on_select_imgitem)
        self.ls_imagefiles_listbox.pack(side="left", fill="both", expand=True)
        self.sc_imagefiles_scorllbar.config(
            command=self.ls_imagefiles_listbox.yview)

        self.log_var = tk.StringVar()
        self.log_var.set("multi image label tool! %s" % (_version_))
        self.l_log_message_label = tk.Label(
            master=self.f_loading_file_frame, textvariable=self.log_var, anchor='w')
        self.l_log_message_label.pack(side="bottom", fill="x")

        # ----------------------------
        # right frame for classes and prev and next
        # ----------------------------
        self.f_label_operate_frame = tk.Frame(self.father, borderwidth=5)
        self.f_label_operate_frame.pack(side="right", fill="y")
        self.b_setting_button = tk.Button(
            master=self.f_label_operate_frame, text="setting classes", command=self.on_setting)
        self.b_setting_button.pack(side="top", fill='x')
        self.b_prev_button = tk.Button(
            master=self.f_label_operate_frame, text="prev", width=20, command=self.on_prev)
        self.b_prev_button.pack(side="top", fill='x')

        self.f_label_operate_ratio_frame = tk.Frame(self.f_label_operate_frame)
        self.f_label_operate_ratio_frame.pack(fill="y", anchor="w")
        self.label_ratio_var = tk.StringVar()
        self.label_ratio_list = []
        self._update_ratio_()
        
        # for idx, (class_name, class_value) in enumerate(Classes):
        #     tmp_ratio_button = tk.Radiobutton(self.f_label_operate_ratio_frame, text=class_name, variable=self.label_ratio_var, value=class_value, command=self.on_next)
        #     tmp_ratio_button.pack(side="top", anchor="w")
        #     self.label_ratio_list.append(tmp_ratio_button)
        # self.label_ratio_var.set(Classes[0][1])
        self.b_next_button = tk.Button(
            master=self.f_label_operate_frame, text="next", command=self.on_next)
        self.b_next_button.pack(side="top", fill='x')
        self.b_extract_button = tk.Button(
            master=self.f_label_operate_frame, text="extract files", command=self.on_extract)
        self.b_extract_button.pack(side="top", fill='x')
        

        # ----------------------------
        # center frame for canvas
        # ----------------------------
        self.canvas_frame = tk.Frame(self.father, borderwidth=5)
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas = IVCanvas(
            self.canvas_frame, relief="ridge", borderwidth=5)
        self.canvas.pack(fill="both", expand=True)
        self.file_path_var = tk.StringVar()
        self.file_path_var.set("waiting for image")
        self.l_file_path_label = tk.Label(
            master=self.canvas_frame, textvariable=self.file_path_var)
        self.l_file_path_label.pack(side="bottom", fill='x')

    def _save_config_(self):
        with open("./config.cfg", "w") as cnf:
            cnf.write(str(self.config))

    def _load_config_(self):
        if os.path.exists("./config.cfg"):
            with open("./config.cfg", "r") as cnf:
                self.config = eval(cnf.readline())
            if not isinstance(self.config, dict):
                self.config = {}
        else:
            self.config = {}
        self.config.setdefault("shape", "960x480")
        self.config.setdefault("filetype", "both")
        self.config.setdefault("classes", Classes)

    def _update_ratio_(self):
        if len(self.label_ratio_list) > 0:
            for tmp_ratio_button in self.label_ratio_list:
                tmp_ratio_button.pack_forget()
            self.label_ratio_list.clear()
        for idx, (class_name, class_value) in enumerate(self.config["classes"]):
            tmp_ratio_button = tk.Radiobutton(self.f_label_operate_ratio_frame, text="(%s)%s" % (
                class_value, class_name), variable=self.label_ratio_var, value=class_value, command=self.on_next)
            tmp_ratio_button.pack(side="top", anchor="w")
            self.label_ratio_list.append(tmp_ratio_button)
            if idx == 0:
                self.label_ratio_var.set(class_value)

    def _on_resize_(self, event):
        self.config["shape"] = "%dx%d" % (
            self.father.winfo_width(), self.father.winfo_height())
        self._save_config_()

    def on_prev(self):
        if len(self.imagefiles) == 0:
            return
        if self.now_index == 0:
            tkMessageBox.showwarning(
                title="first image", message="Now is the first image of the dir")
            return
        self.ls_imagefiles_listbox.select_clear(self.now_index)
        self.now_index -= 1
        self.ls_imagefiles_listbox.select_set(self.now_index)
        self.ls_imagefiles_listbox.yview_moveto(
            float(self.now_index)/len(self.imagefiles))
        self.fresh_ratio()
        self.fresh_canvas()

    def on_next(self):
        if len(self.imagefiles) == 0:
            return
        self.label_for_this_image()
        self._set_item_color_(self.now_index,colortype="labeled")
        if (self.now_index + 1) == len(self.imagefiles):
            tkMessageBox.showwarning(
                title="last image", message="Now is the last image of the dir")
            return
        self.ls_imagefiles_listbox.select_clear(self.now_index)
        self.now_index += 1
        self.ls_imagefiles_listbox.select_set(self.now_index)
        self.ls_imagefiles_listbox.yview_moveto(
            float(self.now_index)/len(self.imagefiles))
        self.fresh_ratio()
        self.fresh_canvas()

    def on_select_imgitem(self, event):
        x = self.ls_imagefiles_listbox.curselection()
        self.now_index = x[0]
        self.fresh_ratio()
        self.fresh_canvas()

    def on_select_dir(self):
        selected_dir = tkFileDialog.askdirectory()
        if selected_dir == "":
            return
        else:
            self.image_dir_var.set(os.path.normpath(selected_dir))
            self.e_image_dir_entry.focus_set()
            self.e_image_dir_entry.select_range(0, len(selected_dir))
            self.e_image_dir_entry.icursor(len(selected_dir))
            self.e_image_dir_entry.xview_moveto(len(selected_dir))

    def _check_file_(self, filepath):
        if self.config["filetype"] is None:
            return False
        if self.config["filetype"] == "both":
            return is_image_file(filepath) or is_video_file(filepath)
        elif self.config["filetype"] == "image":
            return is_image_file(filepath)
        elif self.config["filetype"] == "video":
            return is_video_file(filepath)
        else:
            return False

    def on_load_dir(self):
        image_dir = self.e_image_dir_entry.get()
        if not os.path.exists(image_dir):
            tkMessageBox.showwarning(
                title="wrong dir", message="\"%s\" is not found!, please check again!" % (image_dir))
            return
        self.now_index = 0
        self.image_dir = image_dir
        self.imagefiles.clear()
        self.image_files_var.set(self.imagefiles)
        self.ls_imagefiles_listbox.delete(0, tk.END)
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                if not self._check_file_(file):
                    continue
                imagepath = os.path.normpath(
                    os.path.join(root[len(image_dir)+1:], file))
                self.imagefiles.append(imagepath)
                self.log_var.set("Searching: %d images searched!" %
                                 (len(self.imagefiles)))
                self.l_log_message_label.update()
        self.image_files_var.set(self.imagefiles)
        self.ls_imagefiles_listbox.focus_set()
        self._check_list_labeled_()
        if len(self.imagefiles) > 0:
            self.ls_imagefiles_listbox.select_set(self.now_index)
            self.fresh_ratio()
            self.fresh_canvas()
    
    def fresh_ratio(self):
        filename = self.imagefiles[self.now_index]
        labelfilename = filename[:len(
            filename) - len(filename.strip().split('.')[-1])] + "txt"
        labelfilename = os.path.join(os.path.normpath(
            self.image_dir), os.path.normpath(labelfilename))
        if os.path.exists(labelfilename):
            with open(labelfilename, "r") as lf:
                fn, cl = lf.readline().strip().split(" ")
                self.label_ratio_var.set(cl)

    def fresh_canvas(self):
        filename = os.path.join(os.path.normpath(
            self.image_dir), os.path.normpath(self.imagefiles[self.now_index]))
        if is_image_file(filename):
            self.canvas.create_image(filename)
        elif is_video_file(filename):
            self.canvas.create_video(filename)
        else:
            return
        self.log_var.set("Now: %d / %d files" %
                         (self.now_index+1, len(self.imagefiles)))
        self.file_path_var.set(self.imagefiles[self.now_index])
        self.l_file_path_label.update()

    def label_for_this_image(self):
        imgpath = self.imagefiles[self.now_index]
        labelfilepath = imgpath[:len(
            imgpath)-len(imgpath.split(".")[-1])] + "txt"
        labelfilepath = os.path.join(os.path.normcase(
            self.image_dir), os.path.normcase(labelfilepath))
        with open(labelfilepath, "w") as lf:
            lf.write("%s %s" % (imgpath, self.label_ratio_var.get()))

    def on_extract(self):
        extract_root = "Extracted_%s" % (
            datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        extract_root = os.path.join(os.path.dirname(
            os.path.normpath(self.image_dir)), extract_root)
        if not os.path.exists(extract_root):
            os.makedirs(extract_root)
        self.log_var.set("")
        count = 0
        for idx, filename in enumerate(self.imagefiles):
            labelfilename = filename[:len(
                filename) - len(filename.strip().split('.')[-1])] + "txt"
            labelfilename = os.path.join(os.path.normpath(
                self.image_dir), os.path.normpath(labelfilename))
            if os.path.exists(labelfilename):
                with open(labelfilename, "r") as lf:
                    fn, cl = lf.readline().strip().split(" ")
                    if fn == filename:
                        filename = os.path.join(os.path.normpath(
                            self.image_dir), os.path.normpath(filename))
                        objdir = os.path.join(os.path.normpath(
                            extract_root), os.path.normpath(cl))
                        if not os.path.exists(objdir):
                            os.makedirs(objdir)
                        shutil.copy2(filename, objdir)
                        count += 1
            self.log_var.set("Now is extracting: %d / %d, %d images are extracted." %
                             (idx+1, len(self.imagefiles), count))
            self.l_log_message_label.update()
        with open(os.path.join(extract_root,"list.txt"), "w") as lf:
            for root, dirs, files in os.walk(extract_root):
                print(dirs)
                for d in dirs:
                    for _, _, files in os.walk(os.path.join(root, d)):
                        for f in files:
                            lf.write("%s/%s %s\n"%(d, f, d))
                break
        self.log_var.set("Summary %d are extracted! Now: %d / %d images" %
                         (count, self.now_index+1, len(self.imagefiles)))
        self.l_log_message_label.update()
        tkMessageBox.showinfo(title="extract message", message="extract result in \"%s\""%(extract_root))

    def on_setting(self):
        classes = askClassesDialog("Classes Setting", initialvalue=self.config["classes"])
        if classes is None or self.config["classes"] == classes:
            return
        else:
            self.config["classes"] = classes
            self._update_ratio_()
            self._save_config_()
    
    def _set_item_color_(self, index, colortype="labeled"):
        self.ls_imagefiles_listbox.itemconfigure(index, background=Pre_Define_Color[colortype])

    def _check_list_labeled_(self):
        for idx, filename in enumerate(self.imagefiles):
            if self._has_label_(filename):
                self._set_item_color_(idx, "labeled")
            else:
                self._set_item_color_(idx, "unlabeled")
                

    def _has_label_(self, filename):
        labelfilename = filename[:len(
                filename) - len(filename.strip().split('.')[-1])] + "txt"
        labelfilename = os.path.join(os.path.normpath(
            self.image_dir), os.path.normpath(labelfilename))
        if os.path.exists(labelfilename):
            return True
        else:
            return False

# if __name__ == '__main__':
#     window = tk.Tk()
#     cl = ClassLabel(window)
#     tk.mainloop()
