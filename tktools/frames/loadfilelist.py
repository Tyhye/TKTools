#!/usr/bin/env python
# -*- code:utf-8 -*-
'''
 @Author: tyhye.wang 
 @Date: 2018-07-30 17:49:30 
 @Last Modified by:   tyhye.wang 
 @Last Modified time: 2018-07-30 17:49:30 
'''

import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox

import os

DefaultMap = ["white", "darkseagreen"]


class LoadFileListFrame(tk.Frame):
    '''
    Load File List Frame

    Params:
        logdict: {"loglabel": "tk.Label", "logvar":"tk.StringVar"} label and var were combined
        itemstates: ["unlabeled", "labeled"]
        colormap: colors for itemstates
        filecheck: `function` check the file type
        statecheck: `function` check the files state in the list 
    '''

    def __init__(self, master=None, cnf={}, logdict=None,
                 itemstates=None, colormap=DefaultMap,
                 filecheck=lambda x: True, statecheck=None, **kw):
        super(LoadFileListFrame, self).__init__(master=master, cnf=cnf, **kw)

        self.logdict = logdict
        self.itemstates = itemstates
        self.colormap = colormap
        self.filecheck = filecheck
        self.statecheck = statecheck

        self.f_top_frame = tk.Frame(self)
        self.f_top_frame.pack(side="top", fill="x")

        self.root_dir = ""
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            master=self.f_top_frame, width=20, textvariable=self.entry_var)
        self.entry.pack(side="left")
        self.b_dir_select_button = tk.Button(
            master=self.f_top_frame, text="select dir", command=self.on_select_dir)
        self.b_dir_select_button.pack(
            side="left", after=self.entry)
        self.b_load_button = tk.Button(
            master=self.f_top_frame, text="loading files", command=self.on_load_dir)
        self.b_load_button.pack(
            side="left", after=self.b_dir_select_button)

        if self.itemstates is not None:
            self.f_states_frame = tk.Frame(self, borderwidth=5)
            self.f_states_frame.pack(
                side="top", fill="x", after=self.f_top_frame)
            self.itemlabels = []
            for idx, itemstate in enumerate(self.itemstates):
                tmplabel = tk.Label(self.f_states_frame, width=1, text=itemstate, bg=self.colormap[idx],
                                    borderwidth=1, relief='solid')
                tmplabel.pack(side="left", fill="x", expand=True)
                self.itemlabels.append(tmplabel)
            print("============")

        # self.f_label_legend_frame = tk.Frame(self.f_loading_file_frame, borderwidth=5)
        # self.f_label_legend_frame.pack(side="top", fill="x")
        # self.l_labeled_legend_label = tk.Label(self.f_label_legend_frame, text="labeled", bg=Pre_Define_Color["labeled"], borderwidth=1, relief='solid')
        # self.l_labeled_legend_label.pack(side="left",fill="x",expand=True)
        # self.l_unlabeled_legend_label = tk.Label(self.f_label_legend_frame, text="unlabeled", bg=Pre_Define_Color["unlabeled"], borderwidth=1, relief='solid')
        # self.l_unlabeled_legend_label.pack(side="right",fill="x",expand=True)

        self.f_list_frame = tk.Frame(self)
        self.f_list_frame.pack(fill="both", expand=True)

        self.scorllbar = tk.Scrollbar(self.f_list_frame)
        self.scorllbar.pack(side="right", fill="y")
        self.now_index = 0
        self.files = []
        self.files_var = tk.StringVar()
        self.files_var.set(self.files)
        self.listbox = tk.Listbox(self.f_list_frame, borderwidth=3, listvariable=self.files_var,
                                  relief='groove', selectmode="browse",
                                  yscrollcommand=self.scorllbar.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scorllbar.config(command=self.listbox.yview)

    def get_file_paths(self, indexs=None):
        res = []
        for idx in indexs:
            filename = os.path.join(os.path.normpath(self.root_dir),
                                    os.path.normpath(self.files[idx]))
            res.append(filename)
        return res

    def get_all_file_paths(self):
        res = []
        for file in self.files:
            filename = os.path.join(os.path.normpath(self.root_dir),
                                    os.path.normpath(file))
            res.append(filename)
        return res
    
    def get_file_names(self, indexs=None):
        res = []
        for idx in indexs:
            filename = os.path.normpath(self.files[idx])
            res.append(filename)
        return res

    def get_all_file_names(self):
        res = []
        for file in self.files:
            filename = os.path.normpath(file)
            res.append(filename)
        return res
    
    def get_root_dir(self):
        return self.root_dir

    def get_now_index(self):
        return self.now_index

    def set_now_index(self, index):
        self.now_index = index
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(index)

    def bind(self, bindstr, func):
        # bindstr = ""
        frametype, eventstr = bindstr.split("|")
        if frametype == "<ListBox>":
            self.listbox.bind(eventstr, func)
        else:
            raise "Wrong Frame Type"

    def on_select_dir(self):
        selected_dir = tkFileDialog.askdirectory()
        if selected_dir == "":
            return
        else:
            self.entry_var.set(os.path.normpath(selected_dir))
            self.entry.focus_set()
            self.entry.select_range(0, len(selected_dir))
            self.entry.icursor(len(selected_dir))
            self.entry.xview_moveto(len(selected_dir))

    def on_load_dir(self):
        root_dir = self.entry.get()
        if not os.path.exists(root_dir):
            tkMessageBox.showwarning(
                title="wrong dir", message="\"%s\" is not found!, please check again!" % (root_dir))
            return
        self.root_dir = os.path.normpath(root_dir)
        self.now_index = 0
        self.files.clear()
        self.files_var.set(self.files)
        self.listbox.delete(0, tk.END)
        self.listbox.update()
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if not self.filecheck(file):
                    continue
                path = os.path.normpath(
                    os.path.join(root[len(root_dir)+1:], file))
                self.files.append(path)
                if self.logdict is not None:
                    self.logdict["logvar"].set("Searching: %d files searched!" %
                                               (len(self.files)))
                    self.logdict["loglabel"].update()
                self.listbox.insert(tk.END, path)
                self.listbox.update()
        self.files_var.set(self.files)
        self.listbox.focus_set()
        if self.statecheck is not None:
            self.statecheck(self)
        if len(self.files) > 0:
            self.listbox.select_set(self.now_index)

    def set_state(self, index, state):
        if state in self.itemstates:
            self.listbox.itemconfigure(
                index, background=self.colormap[self.itemstates.index(state)])


# if __name__ == '__main__':
#     window = tk.Tk()
#     var = tk.StringVar()
#     l = tk.Label(window, textvariable=var)
#     l.pack()
#     frame = LoadFileListFrame(window, logdict={
#                               "loglabel": l, "logvar": var},
#                               itemstates=["unlabeled", "labeled"])
#     def func(event):
#         frame.set_state(0, "labeled")
#     frame.bind("<ListBox>|<Button-1>", func)
#     # for i in range(1000):
#     #     mlb.insert(tk.END, ('Important Message: %d' % i, 'John Doe', '10/10/%04d' % (1900+i)))
#     frame.pack(expand=True, fill="both")
#     tk.mainloop()
