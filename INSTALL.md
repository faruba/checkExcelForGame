我是想打包成一个GUI 界面,这样策划随时可以拿过去运行.

依赖库, python main.py 缺什么安装什么吧. 我本地安装的库太多了,很多都有. 印象中要安装 : 
pip install numpy pandas xlrd python-tkdnd openpyxl ply -i https://pypi.tuna.tsinghua.edu.cn/simple

如果要导出 可执行包, 还要装 pyinstaller. **注意:如果要导出,尽量用虚拟环境,只装需要的包,这样打出来的可执行文件比较小.我现在这个打出来也就不到30M,但在我自己的电脑上800多M**

部分文件读取失败, 报错:
*** formula/tFunc unknown FuncID:186
evaluate_name_formula  assert len(tgtobj.stack) == 1 pandas

按照这个 https://stackoverflow.com/questions/29971186/python-xlrd-error-formula-tfunc-unknown-funcid186 
改一下代码, 这个问题比较复杂,他们暂时修不了,要么把那个assert 注释,要么补上一个 186 函数
>>> For now I just wanted to make sure the xlrd read fine. I hacked my xlrd package so that it loads.
>>> 
>>> I don't gaurentee the correctness of the output.
>>> 
>>> Just add the following line in formula.py of your pythonlibs/xlrd package.
>>> 
>>> Around line 240 where each number is map to a function create a hacked function here. I've inserted 'HACKED' in there. I don't understand exactly what's going on.
>>> 
>>> -- added the line that starts with 186:
>>> 
>>> 184: ('FACT', 1, 1, 0x02, 1, 'V', 'V'),
>>> 186: ('HACKED', 1, 1, 0x02, 1, 'V', 'V'), 
>>> 189: ('DPRODUCT', 3, 3, 0x02, 3, 'V', 'RRR'), 
>>> Here is the discussion by xlrd group. Essentially, this is a complicated problem that can't be resolved. :)
>>> 
>>> https://groups.google.com/forum/#!topic/python-excel/ZS5PsC5A6iQ


