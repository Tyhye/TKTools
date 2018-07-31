#!/usr/bin/env python
# -*- code:utf-8 -*-
'''
 @Author: tyhye.wang 
 @Date: 2018-07-30 17:29:06 
 @Last Modified by:   tyhye.wang 
 @Last Modified time: 2018-07-30 17:29:06 
'''

import os
import shutil
import datetime
import random
import _thread

import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox

from ...frames.ivcanvas import IVCanvas
from ...frames.loadfilelist import LoadFileListFrame
from ...frames.multicolumnlistbox import MultiListbox
from ...filecheck import is_image_file, is_video_file
from ..classlabel.classconfig import askClassesDialog

Classes = [
    ("Image1 is better", "0"),
    ("Image2 is better", "1"),
    ("Can't deside", "2"),
]

Pre_Define_Color = {
    "unlabeled": "white",
    "labeled": "darkseagreen"
}

_version_ = "v.0.0.1"


class RankLabel(object):
    min_width = 48
    min_height = 48
    '''
    params:
      filetype: "both", "image", "video", `image` or `video` or `both` files are 
      used for label
    '''

    def __init__(self, master=None):
        if master is None:
            self.father = tk.Tk()
        else:
            self.father = master
        self.father.title("Rank Label")
        self._load_config_()
        self.father.geometry(self.config["shape"])
        self.father.bind("<Configure>", self._on_resize_, add=True)

        # ----------------------------
        # logging of the application
        # ----------------------------
        self.log_var = tk.StringVar()
        self.log_var.set("image rank label tool! %s" % (_version_))
        self.l_log_message_label = tk.Label(
            master=self.father, textvariable=self.log_var, anchor='w')
        self.l_log_message_label.pack(side="bottom", fill="x")
        # ----------------------------
        # left frame for loading files and list
        # ----------------------------
        self.image_dir = ""
        self.imagefiles = []
        self.f_loading_file_frame = LoadFileListFrame(self.father, logdict={"loglabel": self.l_log_message_label, "logvar": self.log_var},
                                                      filecheck=self._check_file_)
        self.f_loading_file_frame.pack(side="left", fill="y")

        # self.f_loading_file_top_frame = tk.Frame(self.f_loading_file_frame)
        # self.f_loading_file_top_frame.pack(side="top", fill="x")

        # self.image_dir = ""
        # self.image_dir_var = tk.StringVar()
        # self.e_image_dir_entry = tk.Entry(
        #     master=self.f_loading_file_top_frame, width=20, textvariable=self.image_dir_var)
        # self.e_image_dir_entry.pack(side="left")
        # self.b_image_dir_select_button = tk.Button(
        #     master=self.f_loading_file_top_frame, text="select dir", command=self.on_select_dir)
        # self.b_image_dir_select_button.pack(
        #     side="left", after=self.e_image_dir_entry)
        # self.b_image_dir_load_button = tk.Button(
        #     master=self.f_loading_file_top_frame, text="loading files", command=self.on_load_dir)
        # self.b_image_dir_load_button.pack(
        #     side="left", after=self.b_image_dir_select_button)

        # self.f_label_legend_frame = tk.Frame(self.f_loading_file_frame, borderwidth=5)
        # self.f_label_legend_frame.pack(side="top", fill="x")
        # self.l_labeled_legend_label = tk.Label(self.f_label_legend_frame, text="labeled", bg=Pre_Define_Color["labeled"], borderwidth=1, relief='solid')
        # self.l_labeled_legend_label.pack(side="left",fill="x",expand=True)
        # self.l_unlabeled_legend_label = tk.Label(self.f_label_legend_frame, text="unlabeled", bg=Pre_Define_Color["unlabeled"], borderwidth=1, relief='solid')
        # self.l_unlabeled_legend_label.pack(side="right",fill="x",expand=True)

        # self.now_index = 0
        # self.imagefiles = []
        # self.image_files_var = tk.StringVar()
        # self.image_files_var.set(self.imagefiles)
        # self.f_loading_file_list_frame = tk.Frame(self.f_loading_file_frame)
        # self.f_loading_file_list_frame.pack(fill="both", expand=True)

        # self.sc_imagefiles_scorllbar = tk.Scrollbar(
        #     self.f_loading_file_list_frame)
        # self.sc_imagefiles_scorllbar.pack(side="right", fill="y")
        # self.ls_imagefiles_listbox = tk.Listbox(self.f_loading_file_list_frame, borderwidth=3, listvariable=self.image_files_var,
        #                                         relief='groove', selectmode="browse", yscrollcommand=self.sc_imagefiles_scorllbar.set)

        # self.ls_imagefiles_listbox.bind(
        #     "<ButtonRelease-1>", self.on_select_imgitem)
        # self.ls_imagefiles_listbox.pack(side="left", fill="both", expand=True)
        # self.sc_imagefiles_scorllbar.config(
        #     command=self.ls_imagefiles_listbox.yview)

        # self.log_var = tk.StringVar()
        # self.log_var.set("multi image label tool! %s" % (_version_))
        # self.l_log_message_label = tk.Label(
        #     master=self.f_loading_file_frame, textvariable=self.log_var, anchor='w')
        # self.l_log_message_label.pack(side="bottom", fill="x")

        # ----------------------------
        # right frame for classes and prev and next
        # ----------------------------
        self.f_label_operate_frame = tk.Frame(self.father, borderwidth=5)
        self.f_label_operate_frame.pack(side="right", fill="y")
        self.b_setting_button = tk.Button(
            master=self.f_label_operate_frame, text="setting classes", command=self.on_setting)
        self.b_setting_button.pack(side="top", fill='x')
        self.generator = None
        self.b_generate_button = tk.Button(
            master=self.f_label_operate_frame, text="generate pairs", command=self.on_generate)
        self.b_generate_button.pack(side="top", fill='x')
        self.b_prev_button = tk.Button(
            master=self.f_label_operate_frame, text="prev", width=20, command=self.on_prev)
        self.b_prev_button.pack(side="top", fill='x')

        self.f_label_operate_ratio_frame = tk.Frame(self.f_label_operate_frame)
        self.f_label_operate_ratio_frame.pack(fill="y", anchor="w")
        self.label_ratio_var = tk.StringVar()
        self.label_ratio_list = []
        self._update_ratio_()

        self.b_next_button = tk.Button(
            master=self.f_label_operate_frame, text="next", command=self.on_next)
        self.b_next_button.pack(side="top", fill='x')
        self.b_extract_button = tk.Button(
            master=self.f_label_operate_frame, text="extract files", command=self.on_extract)
        self.b_extract_button.pack(side="top", fill='x')

        # ----------------------------
        # center frame for canvas
        # ----------------------------
        self.f_rank_frame = tk.Frame(self.father, borderwidth=5)
        self.f_rank_frame.pack(fill="both", expand=True)
        # self.pair_list_frame = tk.Frame(self.f_rank_frame, height=1)
        # self.pair_list_frame.pack(side="top", fill="x", expand=True)

        pair_list_titles = [("image1", 10), ("image2", 10)]
        self.ml_pair_listbox = MultiListbox(
            self.f_rank_frame, lists=pair_list_titles, height=1, selectmode="browse")
        self.ml_pair_listbox.pack(side="top", fill="both", expand=True)
        self.ml_pair_listbox.bind("<ButtonRelease-1>", self.on_select_pairitem)

        self.image1 = None
        self.image2 = None
        self.f_canvas_frame = tk.Frame(self.f_rank_frame, height=1)
        self.f_canvas_frame.pack(side="bottom", fill="both", expand=True)
        self.f_canvas_frame_1 = tk.Frame(self.f_canvas_frame, width=1)
        self.f_canvas_frame_1.pack(side="left", fill="both", expand=True)
        self.file_path_var1 = tk.StringVar()
        self.file_path_var1.set("waiting for image")
        self.l_file_path_label1 = tk.Label(
            master=self.f_canvas_frame_1, textvariable=self.file_path_var1)
        self.l_file_path_label1.pack(side="bottom", fill='x')
        self.canvas1 = IVCanvas(
            self.f_canvas_frame_1, relief="ridge", borderwidth=5, width=1)
        self.canvas1.pack(side="top", fill="both", expand=True,
                          after=self.l_file_path_label1)

        self.f_canvas_frame_2 = tk.Frame(self.f_canvas_frame, width=1)
        self.f_canvas_frame_2.pack(side="right", fill="both", expand=True)
        self.file_path_var2 = tk.StringVar()
        self.file_path_var2.set("waiting for image")
        self.l_file_path_label2 = tk.Label(
            master=self.f_canvas_frame_2, textvariable=self.file_path_var2)
        self.l_file_path_label2.pack(side="bottom", fill='x')
        self.canvas2 = IVCanvas(
            self.f_canvas_frame_2, relief="ridge", borderwidth=5, width=1)
        self.canvas2.pack(side="top", fill="both", expand=True,
                          after=self.l_file_path_label2)

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

    def generator_func(self):
        # self.imagefiles = self.imagefiles[:8]
        random.shuffle(self.imagefiles)
        count = len(self.imagefiles)
        idx = 0
        while (idx+1) < count:
            yield (self.imagefiles[idx], self.imagefiles[idx+1])
            idx += 2
        idx = 1
        while (idx+1) < count+1:
            if idx+1 == count:
                idy = 0
            else:
                idy = idx + 1
            yield (self.imagefiles[idx], self.imagefiles[idy])
            idx += 2
        if count % 2 == 1:
            yield (self.imagefiles[0], self.imagefiles[count-1])
        inter = 2
        while inter < (count - 1):
            idx = 0
            while (idx + inter) < count:
                yield (self.imagefiles[idx], self.imagefiles[idx+inter])
                idx += 1
            inter += 1

    def on_generate(self):
        if self.generator is None or self.image_dir != self.f_loading_file_frame.get_root_dir():
            self.ml_pair_listbox.delete(0, tk.END)
            self.now_index = 0
            self.image_dir = self.f_loading_file_frame.get_root_dir()
            self.imagefiles = self.f_loading_file_frame.get_all_file_names()
            count = 0
            random.seed(0)
            self.generator = self.generator_func()
        for _ in range(1000):
            try:
                pair = list(next(self.generator))
                pair.sort()
                image1, image2 = pair
                self.ml_pair_listbox.insert(tk.END, (image1, image2))
            except StopIteration:
                tkMessageBox.showwarning(
                    title="last pair", message="Now is the last pair!")
                break
        self._check_list_labeled_()
        self.ml_pair_listbox.selection_set(self.now_index)
        self.image1, self.image2 = self.ml_pair_listbox.get(self.now_index)
        self.fresh_ratio()
        self.fresh_canvas()

    def on_prev(self):
        if self.ml_pair_listbox.size() == 0:
            return
        if self.now_index == 0:
            tkMessageBox.showwarning(
                title="first pair", message="Now is the first pair of the images")
            return
        self.ml_pair_listbox.selection_clear(self.now_index)
        self.now_index -= 1
        self.ml_pair_listbox.selection_set(self.now_index)
        self.ml_pair_listbox.yview_moveto(float(self.now_index)/self.ml_pair_listbox.size())
        self.image1, self.image2 = self.ml_pair_listbox.get(self.now_index)
        self.fresh_ratio()
        self.fresh_canvas()

    def on_next(self):
        if self.ml_pair_listbox.size() == 0:
            return
        self.label_for_this_image()
        self._set_item_color_(self.now_index, colortype="labeled")
        if (self.now_index + 1) == self.ml_pair_listbox.size():
            self.on_generate()
            if (self.now_index + 1) == self.ml_pair_listbox.size():
                # tkMessageBox.showwarning(
                # title="last pair", message="Now is the last image of the dir")
                return
        self.ml_pair_listbox.selection_clear(self.now_index)
        self.now_index += 1
        self.ml_pair_listbox.selection_set(self.now_index)
        self.ml_pair_listbox.yview_moveto(float(self.now_index)/self.ml_pair_listbox.size())
        self.image1, self.image2 = self.ml_pair_listbox.get(self.now_index)
        self.fresh_ratio()
        self.fresh_canvas()

    def on_select_pairitem(self, event):
        x = self.ml_pair_listbox.curselection()
        self.now_index = x[0]
        self.image1, self.image2 = self.ml_pair_listbox.get(self.now_index)
        self.fresh_ratio()
        self.fresh_canvas()

    # def on_select_dir(self):
    #     selected_dir = tkFileDialog.askdirectory()
    #     if selected_dir == "":
    #         return
    #     else:
    #         self.image_dir_var.set(os.path.normpath(selected_dir))
    #         self.e_image_dir_entry.focus_set()
    #         self.e_image_dir_entry.select_range(0, len(selected_dir))
    #         self.e_image_dir_entry.icursor(len(selected_dir))
    #         self.e_image_dir_entry.xview_moveto(len(selected_dir))

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

    # def on_load_dir(self):
    #     image_dir = self.e_image_dir_entry.get()
    #     if not os.path.exists(image_dir):
    #         tkMessageBox.showwarning(
    #             title="wrong dir", message="\"%s\" is not found!, please check again!" % (image_dir))
    #         return
    #     
    #     self.image_dir = image_dir
    #     self.imagefiles.clear()
    #     self.image_files_var.set(self.imagefiles)
    #     self.ls_imagefiles_listbox.delete(0, tk.END)
    #     for root, dirs, files in os.walk(image_dir):
    #         for file in files:
    #             if not self._check_file_(file):
    #                 continue
    #             imagepath = os.path.normpath(
    #                 os.path.join(root[len(image_dir)+1:], file))
    #             self.imagefiles.append(imagepath)
    #             self.log_var.set("Searching: %d images searched!" %
    #                              (len(self.imagefiles)))
    #             self.l_log_message_label.update()
    #     self.image_files_var.set(self.imagefiles)
    #     self.ls_imagefiles_listbox.focus_set()
    #     self._check_list_labeled_()
    #     if len(self.imagefiles) > 0:
    #         self.ls_imagefiles_listbox.select_set(self.now_index)
    #         self.fresh_ratio()
    #         self.fresh_canvas()

    def _get_label_file_name_(self, pair=None):
        if pair is None:
            image1 = self.image1
            image2 = self.image2
        else:
            image1, image2 = pair    
        labelfilename = image1[:-(len(image1.strip().split('.')[-1])+1)] + \
            '-' + \
            image2[:-(len(image2.strip().split('.')[-1])+1)] + '.txt'
        labelfilename = os.path.join(os.path.normpath(
            self.image_dir), os.path.normpath(labelfilename))
        return labelfilename

    def fresh_ratio(self):
        labelfilename = self._get_label_file_name_()
        if os.path.exists(labelfilename):
            with open(labelfilename, "r") as lf:
                image1, image2, cl = lf.readline().strip().split(" ")
                self.label_ratio_var.set(cl)

    def fresh_canvas(self):
        if self.image1 is not None:
            filename = os.path.join(os.path.normpath(
                self.image_dir), os.path.normpath(self.image1))
            # print(filename)
            if is_image_file(filename):
                self.canvas1.create_image(filename)
            elif is_video_file(filename):
                _thread.start_new_thread(self.canvas1.create_video, (filename,))
            else:
                return
            self.file_path_var1.set(self.image1)
            self.l_file_path_label1.update()
        if self.image2 is not None:
            filename = os.path.join(os.path.normpath(
                self.image_dir), os.path.normpath(self.image2))
            # print(filename)
            if is_image_file(filename):
                self.canvas2.create_image(filename)
            elif is_video_file(filename):
                _thread.start_new_thread(self.canvas2.create_video, (filename,))
                # self.canvas2.create_video(filename)
            else:
                return
            self.log_var.set("Now: %d / %d pair" %
                             (self.now_index+1, self.ml_pair_listbox.size()))
            self.file_path_var2.set(self.image2)
            self.l_file_path_label2.update()

    def label_for_this_image(self):
        labelfilepath = self._get_label_file_name_()
        with open(labelfilepath, "w") as lf:
            lf.write("%s %s %s" % (os.path.normpath(self.image1), os.path.normpath(self.image2), self.label_ratio_var.get()))

    def on_extract(self):
        pairs = self.ml_pair_listbox.get(0, tk.END)
        if len(pairs) == 0:
            return
        extract_file = "extracted_%s.txt" % (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        extract_file = os.path.join(os.path.normpath(self.image_dir), extract_file)
        with open(extract_file, "w") as exf:
            count = 0
            for idx, pair in enumerate(pairs):
                labelfilename = self._get_label_file_name_(pair)
                if os.path.exists(labelfilename):
                    with open(labelfilename, "r") as lf:
                        # print(labelfilename)
                        line = lf.readline()
                        exf.write("%s\n"%(line.strip()))
                        count += 1
                        self.log_var.set("Now is extracting: %d / %d, %d pairs are extracted." %
                             (idx+1, self.ml_pair_listbox.size(), count))
                        self.l_log_message_label.update()        
        self.log_var.set("Summary %d are extracted! Now: %d / %d images" %
                         (count, self.now_index+1, self.ml_pair_listbox.size()))
        self.l_log_message_label.update()
        tkMessageBox.showinfo(title="extract message", message="%d pairs are extracted in \"%s\""%(count, extract_file))

    def on_setting(self):
        classes = askClassesDialog(
            "Classes Setting", initialvalue=self.config["classes"])
        if classes is None or self.config["classes"] == classes:
            return
        else:
            self.config["classes"] = classes
            self._update_ratio_()
            self._save_config_()

    def _set_item_color_(self, index, colortype="labeled"):
        self.ml_pair_listbox.itemconfigure(
            index, background=Pre_Define_Color[colortype])

    def _check_list_labeled_(self):
        pairs = self.ml_pair_listbox.get(0, tk.END)
        for idx, pair in enumerate(pairs):
            # print(pair)
            labelfilename = self._get_label_file_name_(pair)
            if os.path.exists(labelfilename):
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
