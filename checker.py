import ast
import jpath
import myTp
from numpy import nan
import numpy as np
import pandas as pd
from datetime import datetime
import sys
import re

TP_NUM = [int, float]
TP_LIST = [list, set, dict]
def betterPrint(mask,env, colData):
    #m2 = colData[~mask]
    ret = env.curTableData.loc[~mask,[env.curMainKey, mask.name]]
    #print("=====?", env.curTableData, mask, ret, colData[~mask])
    #return ret
def getTp(v):
    #if(v == "NaN"):
    #print("+====",v, type(v))
    try:
        if(pd.isna(v)):
            return 'NA'
    except ValueError as e:
        pass
    tp = type(v)
    #print(v,"====?", tp, pd.isna(v), tp == myTp.Color)
    if(tp == myTp.Color):
        return 'Color'
    if(tp in TP_NUM):
        return 'Number'
    elif(tp == str):
        return 'String'
    elif(tp in TP_LIST):
        #必须是字符存类型,否则uniq 会失败
        #ret = str(list(map(getTp,v))).replace("'","")
        ret = str(list(map(getTp,v)))#.replace("'","")
        #print("=======", tp, v, ret)
        return ret
    return tp

def _checTimeByStr(v,allDateStrList):
    for dstr in allDateStrList:
        try:
            if(bool(datetime.strptime(v.replace('"',""),dstr))):
                return True
        except ValueError:
            pass
    return False

def CkRange(colValus, args):
    #print("===tp", colValus.dtype, colValus)
    isList, colValus =  tryConvetList(colValus)
    colValus = colValus.fillna('NA')
    #print("==_range", isList, colValus)

    if(args[1] == "Array"):
        if(isList):
            def isIn(x):
                if(isinstance(x,list)):
                    return x.issubset(args[0])
                else:
                    return x in args[0]

            #print("======?", args, colValus)
            #mask = colValus.apply(lambda x: x.issubset(args[0]))
            mask = colValus.apply(isIn)
        else:
            mask = colValus.isin(args[0])
    elif(args[1] == "FromTo"):
        if(isList):
            mask = colValus.apply(lambda x: all(y>=args[0][0] and y <=args[0][1] for y in x))
        else:
            #print("=========?", args[0], type(args[0][0]), colValus)
            mask = colValus.between(args[0][0], args[0][1])
    else:
        return False, None, "不支持该配置,只支持 Array,FromTo"

    return mask.all(), mask, ""

def CkTime(colValus, arg):
    mask = colValus.apply(_checTimeByStr, args = (arg[0].split('|'),))
    return mask.all(), mask, ""

customTypeCheckFunc = {
    "Time":CkTime,
    "Range":CkRange,
}
arrReg = r'([a-zA-Z_][a-zA-Z_0-9]*)'
repReg = r"'\1'"
toList = str.maketrans({"{":"[","}":"]"})
def toarr(v):
    if(type(v) == list):
        return v
    if(not str.startswith(v,"{")): #"}" 
        return v
    nv1 = v.translate(toList)
    nv = re.sub(arrReg, repReg,nv1)
    #print("========cast", nv, nv1)
    return ast.literal_eval(nv)
def tryConvetList(colValus):
    isList = False
    if(colValus.dtype == 'object'):
        try:
            colValus = colValus.apply(toarr)
            #colValus = colValus.apply(ast.literal_eval)
            isList = True
        except Exception as e:
            #print("===cast fail", e, )
            pass

    return isList, colValus

def splitByDot(v):
    return v.split('.')

def array_depth(arr):
    if not arr:
        return 0
    if isinstance(arr[0], list):
        return 1 + array_depth(arr[0])
    else:
        return 1
def groupByLen(cfg):
    spCfg = cfg.split("|")
    if(len(spCfg) == 1):
        return True, spCfg[0].split('.')
    ret = {}
    for sp in spCfg:
        spL = sp.split('.')
        ret[len(spL)] = spL
    return False, ret
def _pickByPath(colValus, path):
    #if(str.startswith(path,"@")):
    #    v = ast.literal_eval(path.replace("@"))
    #    print("========pick", path, v)
    #    return pd.Series([v],copy=False)
    isSingle, segsList = groupByLen(path)

    def helper(obj):
        if(path == "*" and not isinstance(obj, list)):
            #print("========??", obj, type(obj))
            return [obj]   
        if(isSingle):
            segs = segsList
        else:
            dep = array_depth(obj)
            segs = segsList.get(dep)
        if(segs is None):
            return obj
        #if(colValus.name == "PreTask"):
        #    print("==========?", obj, type(obj), path)
        if len(segs) == 1 and segs[0] == jpath.SELF:
            return [int('0'.join(map(str,obj)))]
        else:
            ret = {}
            jpath._iter_match(obj, segs, 0, [], ret)
            v = ret.values()
            #print("=======?", v)
            ret = list(set(v))
            #if(not isSingle):
            #print("===iS", segsList, segs,obj, ret)
            #print("===========pic", ret, path, segs, obj)
        return ret
    return colValus.apply(helper)

def pickByIdx(v, idx):
    #print("====pick", v,idx)
    try:
        return v[idx]
    except Exception as e:
        return None
        #print("WrongData", v, type(v), idx)
        #raise e
def __Type(colValus, args, env):
    if(len(sys.argv) >=3 and sys.argv[2] != colValus.name):
        print(">>ignore", colValus.name, sys.argv[2])
        return True, "Ignore"
    #print("----", args, len(args), env.curCol)
    # 如果Type 传入多参数,是希望N选1,所以全不过才算失败
    if(len(args) > 1):
        dataTps = colValus.apply(getTp).unique()
        for dtp in dataTps:
            #print("=========dtpTYP", type(dtp), dtp, dataTps, dtp in dataTps, dtp == dataTps[0])
            #if(isinstance(dtp, list)):
            #    dtp = str(list(map(getTp,dtp))).replace("'","")
            #    print("======??", dtp, args)
            if(dtp in dataTps):
                #print("=======ok", args, dataTps)
                return True,""
        return False, f"文件:[{env.curFileName}] 列:[{colValus.name}]需要类型{args}之一,但实际类型为{dtp}"

    for tp in args:
        #print("====", tp)
        if(isinstance(tp, str)):
            dataTps = colValus.apply(getTp).unique()
            #print("==== 1", tp, dataTps)
            #print("====?", args, dataTps)
            if(tp not in dataTps):
                return False, f"12 文件:[{env.curFileName}] 列:[{colValus.name}]需要类型{tp}之一,但实际类型为{dataTps}"
        if(isinstance(tp, list)):
            #pass
            colValus= colValus.dropna()
            isList, colValus =  tryConvetList(colValus)
            if(not isList):
                return False, f"文件:[{env.curFileName}] 列:[{colValus.name}]传入数值非数组({colValus}),格式不匹配{tp}"
            idx = 0
            #print("======list tp", tp, isList)
            #print("=list==befor", tp, colValus)
            for subTp in tp:
                elmV = colValus.apply(pickByIdx,args=(idx,))
                #print("========check", elmV)
                sIsOk, sMsg = __Type(elmV,[subTp],env)
                if(not sIsOk):
                    return False, sMsg
                idx+=1
        elif(isinstance(tp, tuple)):
            fname = tp[1]
            param = tp[2]
            #print("=====", tp)
            if(fname not in  customTypeCheckFunc):
                return False, f"文件:[{env.curFileName}] 找程序实现检查函数{fname}"
            fn = customTypeCheckFunc[fname]
            isOk, mask, msg = fn(colValus, param)
            if(not isOk):
                return False, f"文件:[{env.curFileName}] 类型检查失败{colValus[~mask]} 需要{param},{msg}"
    return True, ""

def __Uniq(colValus,args,env):
    # Logical operators for Boolean indexing in Pandas
    dupVals = colValus.value_counts()[colValus.value_counts() > 1]
    isDup = len(dupVals) >= 1
    if(isDup):
        return False, f"文件:[{env.curFileName}] 表中存在重复的建 [重复的建,重复次数]:{dupVals}"
    else:
        return True,""

EMPTY = pd.DataFrame([])
def __In(colValus,args,env):
    #如果没有配置,说明不关心,所以要先移除 NA
    colValus= colValus.dropna()
    #if(colValus.dtype == 'float64'):
    #    colValus = colValus.astype(int, copy=False)
    if(args[0]=="@"):
        tData = env.curTableData.get(args[1])
    #elif(str.startswith(args[0], "@@")):
    #    pass
    #    #tData = pd.pd.Series()
    else:
        tData = env.table.getFile(args[0])
        if(tData.empty):
            return False, f"文件:[{env.curFileName}] IN:文件不存在,请检查配置:{args}"
        if(args[1] == "*"):
            #print("=====args", args, tData.columns)
            tData = tData.columns
            pass
        else:
            tData = tData.get(args[1],EMPTY)

    if(tData.empty):
        return False, f"文件:[{env.curFileName}] 验证列不存在,请查看配置:{args}"
    

    if(len(args) == 3):
        isList, colValus =  tryConvetList(colValus)
        needPick = True
        if(not isList):
            if(args[2].startswith("@")):
                colValus = pd.Series([ast.literal_eval(args[2][1:])])
                needPick = False
                #print("====h", colValus)
            elif(args[2] != "*"):
                #print("=2===h", args[2], args[2].startswith("@"))
                return False, f"文件:[{env.curFileName}] 目标数据不是数组结构,不应配置第3参数:{args}"
        #print("========IN", args, colValus)
        try:
            if(needPick):
                colValus = _pickByPath(colValus,args[2])
        except:
            return False, f"文件:[{env.curFileName}] 列[{env.curCol}] 数组结构无法匹配第三参数{ args}, 请检查数据结构"
        #print("====after", colValus, tData)
        mask = colValus.apply(lambda x: pd.Series(x).isin(tData).all())
        #print("===mask", mask)
    else:
        mask = colValus.isin(tData)

    if(not mask.all()):
        result = colValus[~mask]
        return False, f"文件:[{env.curFileName}] 目标列中 {args}不存在该值:\n{result}"
    return True, ""
def __Range(colValus,args,env):
    #print("===?", env.curTableData)
    isOk, ret, msg = CkRange(colValus, args)
    if(not isOk):
        if(ret is None):
            return False, msg
        return False, f"文件:[{env.curFileName}] 目标列中不存在该值:\n{colValus[~ret]}, 希望:{args}"
    return True, ""
funs = {
        "Type":__Type,
        "Range":__Range,
        "IN"   :__In,
        "Uniq" :__Uniq,
}
