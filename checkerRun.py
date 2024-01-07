# -*- coding: utf-8 -*-
#下面这些本质上就是ast解释器.如果看我实现的relationship.lua 就会发现两者很相似.
#用SICP 中的一句话,用LISP 编成,本质上就是用LISP 写一个语言解释器,然后用这门新语言
#开发功能. 从某种角度上说,这也是编成的本质.
import mycfg
import tableCache
import parse
import checker
import pprint
import os
import sys
import pandas as pd

def getColData(data, col):
    return data[col]

predicateFun = {
        ">=":  lambda v1,v2 : v1 >=  v2,
        ">":   lambda v1,v2 : v1 >   v2,
        "=":   lambda v1,v2 : v1 ==  v2,
        "<=":  lambda v1,v2 : v1 <=  v2,
        "<":   lambda v1,v2 : v1 <   v2,
        "!=":  lambda v1,v2 : v1 !=  v2,
        #"or":  lambda v1,v2 : v1 or  v2,
        #"and": lambda v1,v2 : v1 and v2,
}
EMPTY_ARR = []
# python 真TMD爽!!!,爱死这个机制了,
#[ColName.Number cmp xxx] 的模式会转换成 @getByIdx(ColName,Number) cmp xxx
#的格式. pandas query不支持列表, 现在支持了
def pick(v, idx):    
    if(v is pd.NA):
        return v
    else:
        return v[idx]      
def getByIdx(x,idx):
    ret = x.apply(pick, args=(idx,)) 
    return ret   
def pickByPredicate(mode, pred, data, log):
    # 得益于 pandas query, 事情简单多了
    v = mode.curTableData.query(pred)
    return v
    #cmpFun = pred[0]
    #if(cmpFun == "or"):
    #    pass
    #elif(cmpFun == "and"):
    #    pass
    #else:
    #    pfunc = predicateFun[cmpFun]
    #    if(pfunc == None):
    #        log.append(ERROR, f"没有实现Predicate:{cmpFun}")
    #        return None
    #    colName = pred[1]
    #    val = pred[2]
    #    colVal = getColData(self.curTableData, colName)
    #    if(colVal == None):
    #        log.append(ERROR, f"没有要检测的列(Predicate:{cmpFun}): {colName},[{pred}]")
    #        return None
    #    mask = colVal.apply(pfunc,args=(val,))
    #    colVal[mask]

    #return None

def checkCol(self, cfg, data, log):
    colName = cfg[1]
    self.curCol = colName
    log.append("col",colName,f"检查列:{colName}")
    checkList = cfg[2]
    if(colName not in data):
        log.append("error", None, f"{self.curFileName} 不存在该列:{colName}")
        return
    checkData = getColData(data, colName)
    #print("====getD", checkData, data)
    self._walkAst(checkList,checkData,log)

def checkFun(self, cfg, data, log):
    funName = cfg[1]
    if funName not in checker.funs:
        log.append("error", None, f"文件:[{self.curFileName}] 未实现检查函数:{funName}")
        return
    fun = checker.funs[funName]
    try:
        isOk, msg = fun(data, cfg[2], self)
        if not isOk:
            log.append("error",None, f"{funName} 检测失败:{msg}")
    except Exception as e:
        #print("+======", funName)
        pprint.pprint(log)
        print("===curFile", self.curFileName, funName, self.curCol)
        raise e
        #@exit()

# 只有验证通过才求值
def ifCheckFun(self,cfg, data, log):
    pCfg = cfg[1]
    action = cfg[2]
    try:
        needCheckData = pickByPredicate(self, pCfg,data, log)
    except IndexError:
        log.append("error",None,f"文件[{self.curFileName}] 列[{self.curCol}]条件表达式{pCfg}不正确,请检测 下标是否越界")
        return
    except Exception as e:
        log.append("error",None,f"文件[{self.curFileName}] 列[{self.curCol}]条件表达式{pCfg}不正确,请检测")
        #raise e
        return
    #print("=============v", needCheckData[data.name],"action:\n", action, "cfg:\n",cfg)
    if(needCheckData.size > 0):
        checkFun(self, action, needCheckData[data.name], log)

def copyAst(self, cfg, data, log):
    colName = cfg[1]
    cpName = cfg[2]
    oriAst = next(filter(lambda x: x[1] == cpName,self.ast),None)
    if oriAst == None:
        log.append("error",None,f"文件:[{self.curFileName}] @SameAs 仿照的列{cpName} 不存在")
        return
    ast = (oriAst[0],colName, oriAst[2])
    self._excuteCmd(ast, data, log)
    
cmdFuncs = {
        "checkCol":checkCol,
        "checkFun":checkFun,
        "ifCheckFun": ifCheckFun,
        "copyAst": copyAst,
}
class CheckerRun:
    def __init__(self, log):
        self.cfg = mycfg.MyCfg()
        self.table = tableCache.ExcelCache(self.cfg)
        self.parser = parse.MyLexer()
        self.log = log
        log.addChecker(self)
        self.parser.build(log, True)

    def checkByRules(self, includeFiles = None):
        ruleDir = self.cfg.rules()
        files = os.listdir(ruleDir)
        log = self.log
        log.append("begin", [len(files), includeFiles], f"开始检查")
        for fileName in files:
            name, _ext = os.path.splitext(fileName)
            if(includeFiles is not None and name not in includeFiles):
                continue
            log.append("parse", name, f"载入表格规则:{name}")
            with open(os.path.join(ruleDir,fileName),'r',encoding='utf-8') as f:
                print("parse file", name)
                self.curFileName = name
                self.ast = self.parser.parseRule(f, name)
            log.append("check", name, f"检查表格:{name}")
            self.__checkByRule(name, self.ast,log)
            log.append("checkFinish", name, f"检查表格:{name} 完毕")
            if(log.needStop()):
                return

        log.append("finish", None, f"检查完毕")
        #pprint.pprint(log.getErr())
    def __checkByRule(self, name, ast, log):
        data = self.table.getFile(name)
        #data = data.fillna(value = 'Null')
        #如果主键是空,也忽略
        self.curMainKey = data.columns[0]
        self.curTableData = data.dropna(subset=[self.curMainKey])
        if(self.curTableData.size >0):
            #pprint.pprint(ast)
            self._walkAst(ast, data, log)

    def _walkAst(self, ast, data, log):
        if isinstance(ast, list):
            for subAst in ast:
                self._walkAst(subAst, data, log)
        elif isinstance(ast, tuple):
            self._excuteCmd(ast, data, log)

    def _excuteCmd(self, ast, data, log):
        cmd = ast[0]
        func = cmdFuncs.get(cmd)
        if(func  == None):
            log.append("error",None,f"文件:[{self.curFileName}] 没有检测函数:{cmd}")
            return
        func(self, ast, data, log)

