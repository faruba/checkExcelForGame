# -*- coding: utf-8 -*-
from tkinter import *
import guifunc as gi
import mycfg
import os
import genRule as gr
_pathWCfg = [
        ["path", {"reason":"Excel表格路径", "var":mycfg.EXCEL_DIR}],
        ["path", {"reason":"rules路径", "var":mycfg.RULE_DIR}],
        ["path", {"reason":"工作路径", "var":mycfg.WORK_DIR}],
]
def genRule(root, env):
    excel = env.cfg.excelDir()
    rule = env.cfg.rules()
    print(root, env.cfg)
    addFiles = gr.genRules(excel, rule)
    env.addLog("添加规则文件")
    for fname in addFiles:
        env.addLog(fname)
    env.addLog("添加规则文件完毕,请完善规则")
def help():
    #gi.openPath()
    pass
def about():
    pass
def openCfgDialog(root, env = None):
    if(env is None):
        env = root
    gi.createDialog(root, _pathWCfg, env)

_menuCfg = [
        {
            "name":"设置",
            "child":[
                {"cmd":"目录","action":openCfgDialog, "key":"Ctrl+o"},
            ]
        },
        {
            "name":"工具",
            "child":[
                {"cmd":"自动生成规则文件","action":genRule, "key":"Ctrl+l"},
                {"cmd":"文档","action":help, "key":"Ctrl+c"},
                {"cmd":"about","action":about, "key":"Ctrl+c"},
            ]
        }
] 
ST_IDLE = 0
ST_WAIT_STOP = 1
ST_CHECKING = 2
class GUIControler:
    def __init__(self):
        self.__var = {}
    def init(self, layout):
        self.log = []
        self.lastSelect = []
        self.layout = layout
        self.stat = ST_IDLE
        self.__alreadyAdd = False
        gi.genMenu(layout.tk_menu,_menuCfg, self)
        # 创建 DnD 对象
        #dndobj = dnd.DnD(layout)
        # 将 Listbox 绑定到 DnD 对象
        
        self.layout.tk_list_box_errFileList.register_drop_target("*")
        self.layout.tk_list_box_errFileList.bind("<<Drop>>", self.drop)
    # 定义拖放事件的回调函数
    def drop(self, event):
        # 获取拖放的文件名
        files = str.split(event.data," ")
        for fpn in files:
            name = os.path.basename(fpn)
            name, _ext = os.path.splitext(name)
            print("--------fileN", fpn, name)
            # 将文件名添加到 Listbox
            self.layout.tk_list_box_errFileList.insert(END, name)

    def var(self, name):
        if name not in self.__var:
            sv = StringVar(name=name)
            self.__var[name] = sv
            sv.trace("w", self.__updateCfg)
            
        return self.__var[name]

    def needStop(self):
        #print('===checkNeeStop', self.stat)
        if(self.stat == ST_WAIT_STOP):
            self.layout.tk_label_stat.config(text = "等待检查...")
            self.stat = ST_IDLE
            return True
        return False
    
    def addChecker(self, checker):
        self.cfg = checker.cfg
        self.checker = checker
        self.__bindVar()
        self. __updateRuleBySvn()
    def __updateRuleBySvn(self):
        rulesDir = self.cfg.rules()
        gi.svnUp(rulesDir)
    def append(self,reason, arg, msg):
        v = self.layout.tk_progressbar_process["value"]
        #print("========log", reason, arg,msg)
        if(reason == "begin"):
            self.__reset(arg, msg)
        if(reason == "parse"):
            self.__alreadyAdd = False
            self.__curFile = arg
        elif(reason == "check"):
            self.layout.tk_label_stat.config(text = msg)
            self.layout.tk_label_stat.config(text = msg+f" ({v}/{self.checkFileCnt})")
        elif(reason == "checkFinish"):
            v = v+1
            self.layout.tk_progressbar_process["value"] = v
            self.layout.tk_label_stat.config(text = msg+f" ({v}/{self.checkFileCnt})")
        elif(reason == "col"):
            pass
        elif(reason == "error"):
            #print("========Err", self.__curFile, msg)
            if(not self.__alreadyAdd):
                self.layout.tk_list_box_errFileList.insert(END, self.__curFile)
                if(self.__curFile in self.lastSelect):
                    self.layout.tk_list_box_errFileList.selection_set(END)
                    self.layout.tk_list_box_errFileList.itemconfigure(END,bg="#00aa00")
                self.__alreadyAdd = True
            self.addLog(msg)
        elif(reason == "finish"):
            self.stat = ST_IDLE
            #print("=====last", self.lastSelect, self.allErr)
            for item in self.allErr:
                if(item not in self.lastSelect):
                    self.layout.tk_list_box_errFileList.insert(END, item)
            #print("====================")
            self.layout.tk_button_doCheck["text"]="开始检查"

        self.layout.update()

    def check(self,evt):
        #print("===========checkDO", self.stat)
        if(self.stat == ST_IDLE):
            self.__startCheck()
        #elif(self.stat == ST_CHECKING):
        #    self.__stopCheck()

    def removeFileName(self, evt):
        listBox = self.layout.tk_list_box_errFileList
        selected = listBox.curselection()
        if(len(selected) == 0):
            return
        listBox.delete(selected)
    def addFileName(self, evt):
        input = self.layout.tk_input_checkName 
        name = input.get()
        if(name == ""):
            return
        listBox = self.layout.tk_list_box_errFileList
        listBox.insert(END,name)
        input.delete(0,END)
        pass
    def addLog(self, msg):
        self.layout.tk_text_log.config(state="normal")
        self.layout.tk_text_log.insert(INSERT, msg+"\n------------------\n")
        self.layout.tk_text_log.config(state="disabled")

    def __updateCfg(self,*args):
        varname = args[0]
        strVar = self.var(varname)
        v =  strVar.get()
        getattr(self.cfg,varname)(v)

    def __startCheck(self):
        self.stat = ST_CHECKING 
        checkList = self.__getCheckFile()
        #print("=======checkList", checkList)
        self.checker.checkByRules(checkList)
        #self.layout.tk_button_doCheck.config(text="1停止")

    def __stopCheck(self):
        self.stat = ST_WAIT_STOP
        self.layout.tk_label_stat.config(text = "正在停止...")
    def __reset(self, arg, msg):
        size = arg[0] if arg[1] is None else len(arg[1])
        self.checkFileCnt = size
        self.layout.tk_progressbar_process.config(maximum= size, value = 0)
        self.layout.tk_text_log.config(state="normal")
        self.layout.tk_text_log.delete('1.0',END)
        self.layout.tk_text_log.config(state="disabled")
        self.layout.tk_list_box_errFileList.delete(0,END)
        pass

    def __stop(self):
        if(self.stat == ST_WAIT_STOP):
            return
        self.stat = ST_WAIT_STOP
            
    def __bindVar(self):
        needSet = False
        for c in _pathWCfg:
            varname = c[1]["var"]
            v = getattr(self.cfg,varname)()
            if(v == ""):
                needSet = True
            else:
                self.var(varname).set(v)
        if(needSet):
            openCfgDialog(self.layout, self)
    def __getCheckFile(self):
        listBox = self.layout.tk_list_box_errFileList
        selected = listBox.curselection()
        allItem = listBox.get(0,END)
        self.allErr = list(allItem)
        if(len(selected) == 0):
            if(len(allItem)>0):
                self.lastSelect = list(allItem)
                return self.lastSelect
            return None
        ret = list(map(listBox.get, selected))
        self.lastSelect = ret
        return ret


