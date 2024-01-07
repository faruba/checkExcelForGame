# -*- coding: utf-8 -*-
from tkinter import * 
from tkinter import ttk 
import tkinter.scrolledtext as st
from functools import partial
from tkinter.filedialog import askdirectory
import configparser
import os
import uuid
import json

# 我也就那么一搜,还真有, 简直是小工具开发的福音. https://www.pytk.net/ 还是开源的.
# https://github.com/iamxcd/tkinter-helper
# 为了支持拖拽, 要引入这个, 比较尴尬.
import tkinterDnD 
#import tkinterdnd2
"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:788392508
在线反馈:https://support.qq.com/product/618914
"""
from tkinter import *
from tkinter.ttk import *
#class WinGUI(Tk):
class WinGUI(tkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_menu = self.__tk_menu(self)
        self.tk_label_frame_errContinor = self.__tk_label_frame_errContinor(self)
        self.tk_list_box_errFileList = self.__tk_list_box_errFileList( self.tk_label_frame_errContinor) 
        self.tk_input_checkName = self.__tk_input_checkName( self.tk_label_frame_errContinor) 
        self.tk_button_add = self.__tk_button_add( self.tk_label_frame_errContinor) 
        self.tk_button_sub = self.__tk_button_sub( self.tk_label_frame_errContinor) 
        self.tk_text_log = self.__tk_text_log(self)
        self.tk_button_doCheck = self.__tk_button_doCheck(self)
        self.tk_progressbar_process = self.__tk_progressbar_process(self)
        self.tk_label_stat = self.__tk_label_stat(self)

    def __win(self):
        self.title("表格检查工具")
        # 设置窗口大小、居中
        width = 800
        height = 600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.minsize(width=width, height=height)
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_menu(self,parent):
        menu = Menu(parent, type=r"menubar")
        parent.config(menu=menu)
        return menu
    def __tk_label_frame_errContinor(self,parent):
        frame = LabelFrame(parent,text="选择检测",)
        frame.place(relx=0.00, rely=0.03, relwidth=0.24, relheight=0.85)
        return frame
    def __tk_list_box_errFileList(self,parent):
        lb = Listbox(parent, selectmode="extended")
        #lb.insert(0, "Mail")
        #lb.insert(0, "ActivityControl")
        #lb.insert(0, "GhostStar")
        lb.place(relx=0.00, rely=0.04, relwidth=0.99, relheight=0.91)
        return lb
    def __tk_input_checkName(self,parent):
        ipt = Entry(parent, )
        ipt.place(relx=0.00, rely=0.00, relwidth=0.75, relheight=0.04)
        return ipt
    def __tk_button_add(self,parent):
        btn = Button(parent, text="+", takefocus=False,)
        btn.place(relx=0.75, rely=0.00, relwidth=0.12, relheight=0.04)
        return btn
    def __tk_button_sub(self,parent):
        btn = Button(parent, text="-", takefocus=False,)
        btn.place(relx=0.87, rely=0.00, relwidth=0.12, relheight=0.04)
        return btn
    def __tk_text_log(self,parent):
        text = st.ScrolledText(parent, state='disabled')
        text.place(relx=0.28, rely=0.04, relwidth=0.71, relheight=0.80)
        return text
    def __tk_button_doCheck(self,parent):
        btn = Button(parent, text="开始检查", takefocus=False,)
        btn.place(relx=0.08, rely=0.91, relwidth=0.09, relheight=0.06)
        return btn
    def __tk_progressbar_process(self,parent):
        progressbar = Progressbar(parent, mode="determinate",orient=HORIZONTAL,)
        progressbar.place(relx=0.26, rely=0.94, relwidth=0.69, relheight=0.02)
        return progressbar
    def __tk_label_stat(self,parent):
        label = Label(parent,text="",anchor="center", )
        label.place(relx=0.27, rely=0.90, relwidth=0.68, relheight=0.04)
        return label
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_button_sub.bind('<Button>',self.ctl.removeFileName)
        self.tk_button_add.bind('<Button>',self.ctl.addFileName)
        self.tk_button_doCheck.bind('<Button>',self.ctl.check)
        pass
if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
