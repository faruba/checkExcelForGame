import os
import io
import pandas as pd
#尽可能的程序生成rules 文件,目前只是读字段头, 第一个 默认插入唯一 number的验证.然后其他默认加一个Type()
def  readColums(filePath):
    print("---loadF", filePath)
    f = pd.read_excel(io=filePath, header=2)
    #f = f.drop(f.head(1).index)
    #f = f.drop(f.head(2).index)
    col = f.columns
    return col
def  genColums(cols, ret):
    i = 0;
    for col in cols:
        if(str.startswith(col,"Unnamed:")):
            continue
        if(i == 0):
            ret.write(f"{col}=Uniq();Type(Number)\n")
        else:
            ret.write(f"{col}=Type()\n")
        i+=1


def genRules(dir, ruleDir):
    files = os.listdir(dir)
    addFiles = []
    for fileName  in files:
        name, _ext = os.path.splitext(fileName)
        #if(str.startswith(name,".~lock.") or str.startswith(name, "@")):
        if(_ext != ".xls" and _ext != ".xlsx"):
            continue
        savePathName = os.path.join(ruleDir,name)+ ".txt"
        if(not os.path.exists(savePathName)):
            with open(savePathName,"w+") as f:
                colums = readColums(os.path.join(dir, fileName))
                genColums(colums, f)
                f.flush()
            addFiles.append(name)

    return addFiles
#getFileName("/home/faruba/Work/hcrH5/hcrproject_h5/战斗新表/", "./rules/")
