'''
 Copy from the http://code.activestate.com/recipes/52266/,
 tyhye.wang changed it byself to achieve more better performance
 * @Author: tyhye.wang 
 * @Date: 2018-07-09 17:57:41 
 * @Last Modified by:   tyhye.wang 
 * @Last Modified time: 2018-07-09 17:57:41 
'''

import tkinter as tk


class MultiListbox(tk.Frame):
    def __init__(self, master, cnf={}, lists=None, yscrollbar='True', selectmode="browse", **kw):
        super(MultiListbox, self).__init__(master, cnf, **kw)
        self.lists = []

        for l, w in lists:
            frame = tk.Frame(self)
            frame.pack(side="left", expand=True, fill="both")
            tk.Label(frame, text=l, borderwidth=1,
                     relief="raised").pack(fill="x")
            lb = tk.Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                            relief="flat", exportselection=False,
                            selectmode=selectmode)
            lb.pack(expand=True, fill="both")
            self.lists.append(lb)
            if selectmode == "extend":
                lb.bind('<Control-1>', lambda e, s=self: s._ctl1(e.y))
            lb.bind('<B1-Motion>', lambda e, s=self: s._b1motion(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._btn_1(e.y))
            lb.bind('<ButtonRelease-1>', lambda e,
                    s=self: s._btn_release_1(e.y))
            lb.bind('<Leave>', lambda e: 'break', add=True)
            lb.bind('<B2-Motion>', lambda e,
                    s=self: s._b2motion(e.x, e.y), add=True)
            lb.bind('<Button-2>', lambda e,
                    s=self: s._button2(e.x, e.y), add=True)
            # lb.send()
        self.last_row = -1
        frame = tk.Frame(self)
        frame.pack(side="left", fill="y")
        tk.Label(frame, borderwidth=1, relief="raised").pack(fill="x")
        if yscrollbar:
            self.sb = tk.Scrollbar(
                frame, orient="vertical", command=self._scroll)
            self.sb.pack(expand=True, fill="y")
            for lb in self.lists:
                lb['yscrollcommand'] = self._set
        # self.lists[0]['yscrollcommand']=sb.set

    def bind(self, *args):
        for lb in self.lists:
            lb.bind(*args)

    def nearest(self, y):
        return self.lists[0].nearest(y)

    def _ctl1(self, y):
        row = self.lists[0].nearest(y)
        if self.selection_includes(row):
            self.selection_clear(row)
        else:
            self.selection_set(row)

    def _btn_1(self, y):
        self.selection_clear(0, tk.END)
        row = self.lists[0].nearest(y)
        self.selection_set(row)

    def _btn_release_1(self, y):
        self.last_row = -1

    def _b1motion(self, y):
        row = self.lists[0].nearest(y)
        if self.selection_includes(row) and self.last_row != row:
            self.selection_clear(self.last_row)
            self.last_row = row
        else:
            self.selection_set(row)
            self.last_row = row

    def _button2(self, x, y):
        for l in self.lists:
            l.scan_mark(x, y)
        # return 'break'

    def _b2motion(self, x, y):
        for l in self.lists:
            l.scan_dragto(x, y)
        # return 'break'

    def _set(self, *args):
        self.sb.set(*args)
        for l in self.lists:
            l.yview_moveto(args[0])

    def _scroll(self, *args):
        for l in self.lists:
            l.yview(*args)

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first, last))
        return result

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, elements):
        for l, e in zip(self.lists, elements):
            l.insert(index, e)
        # for e in elements:
        #     print(e)
        #     i = 0
        #     for l in self.lists:
        #         l.insert(index, e[i])
        #         i += 1

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

    def itemconfig(self, rowindex, colindex=None, cnf={}, **kw):
        if colindex is None:
            for l in self.lists:
                l.itemconfig(rowindex, cnf={}, **kw)
        elif isinstance(colindex, int):
            self.lists[colindex].itemconfig(rowindex, cfg={}, **kw)
        else:
            raise "colindex must be Int or None"

    def update(self):
        for c in self.winfo_children():
            c.update()

# if __name__ == '__main__':
#     window = tk.Tk()
#     tk.Label(window, text='MultiListbox').pack()
#     mlb = MultiListbox(window, lists=(('Subject', 40), ('Sender', 20), ('Date', 10)))
#     for i in range(100):
#         mlb.insert(tk.END, ('Important Message: %d' % i, 'John Doe', '10/10/%04d' % (1900+i)))
#     mlb.pack(expand=True,fill="both")
#     tk.mainloop()
