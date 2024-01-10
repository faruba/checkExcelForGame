import os
import sys
import subprocess
from functools import partial
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
#  根据配置生成 menu 有孩子节点的要配值 name child,
#  叶节点 cmd, action, key 其中key 可选
# cfg [ {
#    name, 
#    child = [ {
#        name,
#        cmd, action, key
#    }
#    ],
#    cmd, action, key
#  }
# ]
def genMenu(menuBar, cfg, env):
    for menuInfo in cfg:
        if("name" in menuInfo):
            wMenu = Menu(menuBar)
            menuBar.add_cascade(menu=wMenu, label = menuInfo["name"])
        else:
            wMenu = menuBar

        if("cmd" in menuInfo):
            wMenu.add_command(label=menuInfo["cmd"],
                              command = partial(menuInfo["action"], wMenu, env),
                              accelerator=menuInfo.get("key"))

        if("child" in menuInfo):
            genMenu(wMenu, menuInfo["child"], env)

def selectPath(pvar):
    path_ = askdirectory() #使用askdirectory()方法返回文件夹的路径
    if path_ == "":
        pvar.get() #当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
    else:
        #path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
        pvar.set(path_)

def openPath(pvar):
    path = pvar.get()
    try:
        if sys.platform == 'darwin':
            subprocess.check_call(['open', '--', path])
        elif sys.platform.startswith('linux'):
            subprocess.check_call(['xdg-open', path])
        elif sys.platform in ['windows', 'win32']:
            path = os.path.dirname(path+"\\")
            os.startfile(path)
        else:
            print('Unknown platform, cannot open file')
    except:
        print('Could not open file ' + path)

def svnUp(workDir):
    try:
        if sys.platform == 'darwin':
            subprocess.check_call(["svn", "up"],cwd=workDir)
        elif sys.platform.startswith('linux'):
            subprocess.check_call(["svn", "up"],cwd=workDir)
        elif sys.platform in ['windows', 'win32']:
            subprocess.check_call(["tortoiseProc", "/command:update", f'/path:"{workDir}' ,"/closeonend:2"],cwd=workDir)
        else:
            print('Unknown platform, cannot svn up')
    except Exception as e:
        print('无法用svn更新 ', e, workDir)


    #print(dir)
def createPthWidget(root, reason, pStrVar, pos, env):
    Label(root, text=reason).grid(row=pos, column=0)
    Entry(root, textvariable=pStrVar,state="readonly").grid(row=pos, column=1,ipadx=200)
    Button(root, text="路径选择", command=partial(selectPath,pStrVar)).grid(row=pos, column=2)
    Button(root, text="打开文件位置", command=partial(openPath,pStrVar)).grid(row=pos, column=3)
_createFunc = {
        "path" : lambda parent, cfg, pos, env: createPthWidget(parent, cfg["reason"], env.var(cfg["var"]), pos, env)
}
    
def createDialog(parent, cfg, env):
    window = Toplevel(parent)
    for i in range(len(cfg)):
        info = cfg[i]
        func = _createFunc[info[0]]
        func(window, info[1], i, env)

