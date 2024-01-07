import configparser
import os

SEC_FILE_MD5     = "files.md5"
SEC_GLOBAL_INFO  = "global"
EXCEL_DIR        = "excelDir"
WORK_DIR         = "workDir"
CACHE_DIR        = "cache"
RULE_DIR         = "rules"

CFG_PATH = "./config.ini"
CFG_MD5 = "./md5.ini"
TP_MAP = {
        "md5":CFG_MD5,
        "cfg":CFG_PATH
}
class MyCfg:
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(CFG_PATH)
        self.md5 = configparser.ConfigParser()
        self.md5.read(CFG_MD5)
    def saveCfg(self): 
        self._save("cfg",CFG_PATH)
        self._save("md5",CFG_MD5)
    def excelDir(self, newVaule = None):
        return self._getset("cfg",SEC_GLOBAL_INFO,EXCEL_DIR, newVaule)
    def workDir(self, newVaule = None):
        return self._getset("cfg",SEC_GLOBAL_INFO,WORK_DIR, newVaule)
    def rules(self, newVaule = None):
        return self._getset("cfg",SEC_GLOBAL_INFO,RULE_DIR, newVaule)
    def cache(self):
        p =  os.path.join(self._getset("cfg",SEC_GLOBAL_INFO,WORK_DIR), CACHE_DIR)
        if(not os.path.exists(p)):
            os.mkdir(p)
        return p
    def fileMd5(self, name, newVaule = None):
        return self._getset("md5",SEC_FILE_MD5,name, newVaule)
    def _save(self, which, path):
        with open(path, 'w') as configfile:
            getattr(self,which).write(configfile)
    def _getset(self, name, sec, key, value = None):
        cfg = getattr(self, name)
        if(sec not in cfg):
            cfg[sec] = {}
        if(value is None):
            ret = cfg[sec].get(key, "")
            #print("==get", ret, sec, key)
            return ret
        else:
            cfg[sec][key] = value
            self._save(name,TP_MAP[name] )
