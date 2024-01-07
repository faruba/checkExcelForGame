import ply.lex as lex
import ply.yacc as yacc
import logging

INFO = 1
ERROR = 2
class MyLexer(object):
    tokens = (
            'EQUEL',   #等号
            'SEMI',    #分号
            'LPAREN',  #左括号
            'RPAREN',  # 右括号
            'COMMA',   # 逗号
            'SAME',    # SameAs
            'AT',      # @符号
            'LBRACK',  # 左中括号
            'RBRACK',  # 右中括号
            'OR',      # |
            'AND',     # &
            'NAME',    # 列名
            'IFTHEN',  # 条件达成
            'NUMBER',  # 数字
            'STRING',  # 字符串

            'GTE',     #>=
            'GT',      #>
            'LT',      #<
            'LTE',     #<=
            'NEQ',     #!=
    )

    # 定义词法规则
    t_EQUEL   = r'='
    t_SEMI    = r';'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_COMMA   = r','
    t_SAME    = r'@SameAs'
    t_AT      = r'@'
    t_LBRACK  = r'\['
    t_RBRACK  = r'\]'
    t_OR      = r'\|'
    t_AND     = r'&'
    t_IFTHEN  = r'=>'
    t_GTE     = r'>='
    t_GT      = r'>'
    t_LT      = r'<'
    t_LTE     = r'<='
    t_NEQ     = r'!='

    t_NAME = r'[A-Za-z_][A-Za-z0-9_]*'
    #t_STRING = r'"[A-Za-z_@%,\|\(\)][A-Za-z0-9_:\|\[\]\(\)@%]*"'

    #def t_NAME(self, t):
    #    r'[A-Za-z_][A-Za-z0-9_]*'
    #    if(t.value == 'NA'):
    #        t.value = pd.NA
    #    return t

    def t_STRING(self, t):
        r'"[A-Za-z0-9_@%\$,\|\(\)\*\.\'][A-Za-z0-9_:\|\[\]\(\)\*\.@%\$\']*"'
        t.value = t.value.replace('"',"")
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
    #记录行号
    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    # 忽略空白符
    t_ignore  = ' \t'
    # 忽略注释
    t_ignore_COMMENT =  r'\#.*'

    # 定义错误处理函数
    def t_error(self, t):
        self.outLog.append("error",None, f"规则解析错误:Illegal character:{t.value[0]} [{self.curFileName}]")
        t.lexer.skip(1)

    # 创建词法分析器

    start = 'line'
    # 定义语法规则
    def p_line(self, p):
        '''line : line rule
                | rule'''
        if len(p) == 2:
            #print('====1', p[0], p[1] )
            p[0] = [p[1]]
        else:
            #print('====2', p[0], p[1], p[2], p[3] )
            p[0] = p[1] + [p[2]]

    def p_rule(self, p):
        '''rule : NAME EQUEL expr_list
                | NAME EQUEL SAME LPAREN NAME RPAREN'''
        if(len(p) == 4):
            p[0] = ('checkCol', p[1], p[3])
        else:
            #print("====>", len(p))
            p[0] = ('copyAst', p[1], p[5])

    def p_expr_list(self, p):
        '''expr_list : expr_list SEMI expr
                     | expr'''
        if len(p) == 4:
            #print("exp_list:", p[0], p[1], p[2],p[3])
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_expr(self, p):
        '''expr : NAME LPAREN arg_list RPAREN
                | NAME LPAREN empty RPAREN
                | condition IFTHEN expr'''
        #print("==============?", p[1],p[2],p[3])
        if( len(p) == 4):
            p[0] = ('ifCheckFun',p[1], p[3])
        elif p[3] == None:
            p[0] = ('checkFun', p[1], [])
        else:
            p[0] = ('checkFun', p[1], p[3])
            
    def p_empty(self, p):
        'empty :'
    def p_condition(self, p):
        '''condition : LBRACK cond_expr_list RBRACK'''
        p[0] = p[2]
    def p_cmp(self, p):
        '''cmp : EQUEL
               | GTE
               | GT
               | LT
               | LTE
               | NEQ'''
        p[0] = p[1]

    def p_cond_expr_list(self, p):
        '''cond_expr_list : cond_expr_list OR cond_expr_list
                          | cond_expr_list AND cond_expr_list
                          | NAME AT NUMBER cmp STRING
                          | NAME AT NUMBER cmp NAME
                          | NAME AT NUMBER cmp NUMBER
                          | NAME cmp STRING
                          | NAME cmp NAME
                          | NAME cmp NUMBER'''
        if p[2] == '|':
            #p[0] = ('or', p[1], p[3])
            p[0] = f"({p[1]} or {p[3]})"
        elif p[2] == '&':
            #p[0] = ('and', p[1], p[3])
            p[0] = f"({p[1]} and {p[3]})"
        elif p[2] == '=':
            p[0] = f"({p[1]} == {p[3]})"
        elif p[2] == '@':
            cmp = "==" if p[4] == "=" else p[4]
            #print(p,"===============",)
            v = f"'{p[5]}'" if p.slice[5].type == "STRING" else p[5]
            p[0] = f"@getByIdx(`{p[1]}`, {p[3]}) {cmp} {v}"
        else:
            #p[0] = (p[2], p[1], p[3])
            p[0] = f"(`{p[1]}` {p[2]} {p[3]})"

    def  p_cond_expr_list_group(self, p):
        '''cond_expr_list : LPAREN cond_expr_list RPAREN'''
        p[0] = p[2]

    def p_array(self, p):
        '''array : LBRACK array_elm RBRACK'''
        p[0] = p[2]
    def p_array_elm(self, p):
        '''array_elm : array_elm COMMA STRING
                     | array_elm COMMA NUMBER
                     | array_elm COMMA NAME
                     | array_elm COMMA expr
                     | array_elm COMMA array
                     | NAME
                     | NUMBER
                     | expr
                     | array
                     | STRING'''
        if len(p) == 4:
            #print("==art_elm 2===", p[0], p[1], p[2],p[3])
            p[0] = p[1] + [p[3]]
        else:
            #print("==arr_elm 1===", p[0], p[1])
            p[0] = [p[1]]

    def p_arg_list(self, p):
        '''arg_list : arg_list COMMA STRING
                    | arg_list COMMA NAME
                    | arg_list COMMA AT
                    | arg_list COMMA array
                    | arg_list COMMA expr
                    | STRING
                    | NAME
                    | AT
                    | array
                    | expr'''
        if len(p) == 2:
            #print("arg_list:", p[0], p[1])
            p[0] = [p[1]]
        else:
            #print("arg_list:", p[0], p[1], p[3])
            p[0] = p[1] + [p[3]]

    def p_error(self, p):
        self.outLog.append("error",None, f"Syntax error in input!:{p} [{self.curFileName}]")
        #assert(False,"Syntax error in input!", p)

    def build(self, outLog, debug = False):
        self.debug = debug
        self.outLog = outLog
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self,debug=debug)
        if(debug):
            logging.basicConfig(
                level = logging.DEBUG,
                filename = "parselog.txt",
                filemode = "w",
                format = "%(filename)10s:%(lineno)4d:%(message)s"
            )
            self.log = logging.getLogger()

    def parseRule(self, f, fname):
        self.curFileName = fname 
        content = f.read()
        ast = self.parser.parse(content, lexer=self.lexer,tracking=self.debug, debug=self.log)
        self.parser.restart()
        return ast
