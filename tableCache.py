import hashlib
import pandas as pd
import os
import re
import myTp
import numpy as np
import ast


reColor = re.compile("[a-fA-F0-9]{6}")
reStr = r'([a-zA-Z_][a-zA-A0-9_]*)'
xls = [".xls",".xlsx"]
def getFilePathName(fDir, fName, ext):
    if(type(ext) == list):
        for e in ext:
            p = os.path.join(fDir,fName)+e
            if(os.path.exists(p)):
                return p
    else:
        return os.path.join(fDir,fName)+ext
def intFirst(v):
    if(v == ""):
        #return np.NaN
        #return myTp.NaN
        # 这是个坑, panda 默认转float64, 先转为 pd.NA 可以避免这种情况
        return pd.NA
    #elif(len(v) == 6 and reColor.match(v)):
    # 不能在这里解析color, 否则可能导致id错误解读
    #    return myTp.Color(v)
    elif(v.startswith("{") and v.endswith("}")):
        #print("====list", v)
        try:
            v = v.replace("{","[").replace("}","]")
            v = re.sub(reStr,r'"\1"',v)
            return ast.literal_eval(v)
        except:
            return v
    elif(v.isdigit()):
        return int(v)
    return v
class ExcelCache:
    def __init__(self,cfg):
        self.cfg=cfg
        self.cache = {}

    def getFile(self, name):
        f = self.cache.get(name)
        if f != None:
            return f
        fileDir = self.cfg.excelDir()
        cacheDir = self.cfg.cache()
        isNeed, newMd5 = self.__isNeedReload(name, fileDir, cacheDir)
        if(isNeed):
            self.__export2CVS(name, fileDir, cacheDir, newMd5)
            return self.__load2Cache(name,cacheDir)
        else:
            return self.__load2Cache(name,cacheDir)

    def __isNeedReload(self, name, fileDir, cacheDir):
        filePath = getFilePathName(cacheDir, name,".csv")
        oldMd5 = self.cfg.fileMd5(name)
        newMd5 = self.__getFileMd5(name, fileDir)
        if not os.path.exists(filePath) or oldMd5 != newMd5:
            return True, newMd5
        return False, ""

    def __getFileMd5(self,fileName, fileDir):
        path = getFilePathName(fileDir, fileName,xls)
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    def __load2Cache(self, name,cacheDir):
        csv = getFilePathName(cacheDir, name,".csv")
        columns = pd.read_csv(csv, sep='\t', nrows=0).columns
        return pd.read_csv(csv, sep='\t', converters={col: intFirst for col in columns},low_memory=False)
    def __export2CVS(self, name, fileDir, cacheDir, newMd5):
            self.cfg.fileMd5(name, newMd5)
            fpn = getFilePathName(fileDir, name, xls)
            #book = openpyxl.load_workbook(filename=fpn,data_only=True)
            #f = pd.read_excel(book)
            f = pd.read_excel(io=fpn)
            f = f.drop(f.head(1).index)
            f.dropna(how="all",inplace=True)
            csv = getFilePathName(cacheDir, name,".csv")
            f.to_csv(csv, index=False, float_format='%g',encoding="utf-8", header=False, sep='\t')
