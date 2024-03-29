#设计初衷当然是帮助策划检查表格,尽量减少因为表格配置错误导致的程序报错.
#从而减少 
# 1.策划找程序查配置问题
# 2.错误数据更新到外网导致的buy 以及后续的数据修复

# 检查函数肯定是由程序完成,如果可以让策划自己维护检查规则,就更好了,退一万步说,如果策划不维护,
# 检查规则,程序应该也不需要花大力气维护规则.所以我决定设计一个语言,方便做表格检查 ;)

# parse.py 是检查语言(我命名为littleChecker aka: lc) 词法解析器, 依赖于 PLY,如果由编译原理的知识,或者懂Lisp 或 Prolog, 应该很容易看懂. 如果要增加语言机制,就在这里实现
# 列名=验证函数列表,用;分隔,必须所有的验证通过才算通过
# 验证函数接受0到多个参数,参数可以是字符串,数组,token
# 验证函数支持条件开关[]中是条件检查列表,支持 |(or) &(and), ()括号分组, 计算为真才做 => 后面的验证,
# 条件检查 由 列名 判断符号 值组成 (我有些纠结要不要支持函数,这样扩展性无疑是最高的,但一方面觉得,如果条件表达式过于繁琐,通常意味着表结构设计上出现了问题(也不一定,可能只是过于通用,比如活动的 CustomCfg, 道具表的 ItemParam),如果要通用到这种程度才能检查出来,我想做表格翻译或许更容易一些,顺便做个检查就足够了)

# tableCache.py 表格检查的特点就是跨表,策划平时的工作特性是只改部分表格,如果每次都要读取所有的表格,效率是在时低下.这个类主要就是基于md5 检测文件是否变化,然后导出为csv,方便相应的库快速读取.同时提供惰性载入的机制,没有涉及到的表格,没必要读取

# checker.py 检查函数,想支持什么检查,就在这里补充好了

# checkerRun.py 把所有模块整合在一起的类, 解析ast, 调用checker, 对数据进行验证
# mycfg.py 简单的configparser 封装
# layout.py 界面布局,工具生成,但凡不是生成的代码,都不能写在这
# guicontrol.py 所有ui的逻辑写在这个里即可
# guifunc.py 一些比较通用的函数.感觉其他工具可以用得到

# main.py 载入环境,运行 checkerRun.
import checkerRun
import layout
import guicontrol
import argparse
parse = argparse.ArgumentParser(
        prog="Excel Checker",
        description="check Excel by Rules")
parse.add_argument('-mode', default="gui", choices=["gui","cmd"])
parse.add_argument('-f', nargs="*", default=[])
args = parse.parse_args()
ctrl = guicontrol.GUIControler()
gui = layout.Win(ctrl)
cr = checkerRun.CheckerRun(ctrl)

if(args.mode == 'cmd'):
    includeFile = None if len(args.f) == 0 else args.f
    cr.checkByRules(includeFile)
gui.mainloop()
