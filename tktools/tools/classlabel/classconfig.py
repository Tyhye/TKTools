#!/usr/bin/env python
# -*- code:utf-8 -*-
'''
 @Author: tyhye.wang 
 @Date: 2018-07-18 17:41:52 
 @Last Modified by:   tyhye.wang 
 @Last Modified time: 2018-07-18 17:41:52 
'''

import tkinter as tk
import tkinter.messagebox as tkMessagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.simpledialog import Dialog
import os


class ClassConfigDialog(Dialog):
    errormessage = "Not true format."
    def __init__(self, title,
                 prompt=None,
                 initialvalue=None,
                 parent=None):

        if not parent:
            parent = tk._default_root

        self.prompt = prompt
        self.initialvalue = initialvalue

        Dialog.__init__(self, parent, title)

    def destroy(self):
        self.entry = None
        Dialog.destroy(self)

    def body(self, master):
        l_prompt = tk.Label(master, text=self.prompt, anchor="w")
        l_prompt.pack(side="top", fill="x")

        self.t_input_text = ScrolledText(master, name="text", height=10)
        self.t_input_text.pack(fill="both", expand=True)
        if self.initialvalue is not None:
            for classname, classvalue in self.initialvalue:
                self.t_input_text.insert(
                    tk.END, "%s %s\n" % (classname, classvalue))
        return self.t_input_text

    def buttonbox(self):
        box = tk.Frame(self)
        w = tk.Button(box, text="OK", width=10,
                      command=self.ok)
        w.pack(side="left", padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side="left", padx=5, pady=5)
        # self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack(side="bottom")

    def validate(self):
        try:
            result = self.getresult()
        except ValueError:
            tkMessagebox.showwarning(
                "Illegal value",
                self.errormessage + "\nPlease try again",
                parent=self)
            return 0

        self.result = result
        return 1

    def getresult(self):
        results = []
        value = self.t_input_text.get('0.0',tk.END)
        lines = value.strip().split("\n")
        for line in lines:
            if line == "":
                continue
            try:
                classname, classid = line.strip().split(" ")
                results.append((classname, classid))
            except:
                raise ValueError
        return results


def askClassesDialog(title,
               prompt="Input classes(format is \"ClassName ClassID\", Every Line Has One Class):",
               **kw):

    d = ClassConfigDialog(title, prompt, **kw)
    return d.result


# if __name__ == '__main__':
#     window = tk.Tk()

#     def click():
#         results = askClasses("classes")
#         print(results)
#     b = tk.Button(window, text="click", command=click)
#     b.pack()
#     tk.mainloop()
