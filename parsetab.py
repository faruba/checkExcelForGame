
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'lineAND AT COMMA EQUEL GT GTE IFTHEN LBRACK LPAREN LT LTE NAME NEQ NUMBER OR RBRACK RPAREN SAME SEMI STRINGline : line rule\n                | rulerule : NAME EQUEL expr_list\n                | NAME EQUEL SAME LPAREN NAME RPARENexpr_list : expr_list SEMI expr\n                     | exprexpr : NAME LPAREN arg_list RPAREN\n                | NAME LPAREN empty RPAREN\n                | condition IFTHEN exprempty :condition : LBRACK cond_expr_list RBRACKcmp : EQUEL\n               | GTE\n               | GT\n               | LT\n               | LTE\n               | NEQcond_expr_list : cond_expr_list OR cond_expr_list\n                          | cond_expr_list AND cond_expr_list\n                          | NAME AT NUMBER cmp STRING\n                          | NAME AT NUMBER cmp NAME\n                          | NAME AT NUMBER cmp NUMBER\n                          | NAME cmp STRING\n                          | NAME cmp NAME\n                          | NAME cmp NUMBERcond_expr_list : LPAREN cond_expr_list RPARENarray : LBRACK array_elm RBRACKarray_elm : array_elm COMMA STRING\n                     | array_elm COMMA NUMBER\n                     | array_elm COMMA NAME\n                     | array_elm COMMA expr\n                     | array_elm COMMA array\n                     | NAME\n                     | NUMBER\n                     | expr\n                     | array\n                     | STRINGarg_list : arg_list COMMA STRING\n                    | arg_list COMMA NAME\n                    | arg_list COMMA AT\n                    | arg_list COMMA array\n                    | arg_list COMMA expr\n                    | STRING\n                    | NAME\n                    | AT\n                    | array\n                    | expr'
    
_lr_action_items = {'NAME':([0,1,2,4,5,7,9,11,12,13,14,15,18,26,27,29,31,32,34,35,36,37,38,39,40,42,43,44,51,65,66,],[3,3,-2,-1,6,-3,-6,17,19,6,28,6,17,48,-5,-9,17,17,55,-12,-13,-14,-15,-16,-17,-7,60,-8,-4,69,72,]),'$end':([1,2,4,7,9,27,29,42,44,51,],[0,-2,-1,-3,-6,-5,-9,-7,-8,-4,]),'EQUEL':([3,17,48,54,],[5,35,35,35,]),'SAME':([5,],[8,]),'LBRACK':([5,12,13,15,26,43,65,],[11,26,11,11,26,26,26,]),'LPAREN':([6,8,11,18,19,26,31,32,48,60,69,],[12,14,18,18,12,18,18,18,12,12,12,]),'SEMI':([7,9,27,29,42,44,],[13,-6,-5,-9,-7,-8,]),'IFTHEN':([10,30,],[15,-11,]),'STRING':([12,26,34,35,36,37,38,39,40,43,65,66,],[22,46,56,-12,-13,-14,-15,-16,-17,59,67,74,]),'AT':([12,17,43,48,],[23,33,61,33,]),'RPAREN':([12,19,20,21,22,23,24,25,28,29,41,42,44,52,53,55,56,57,58,59,60,61,62,63,64,72,73,74,],[-10,-44,42,44,-43,-45,-46,-47,51,-9,58,-7,-8,-18,-19,-24,-23,-25,-26,-38,-39,-40,-41,-42,-27,-21,-22,-20,]),'RBRACK':([16,29,42,44,45,46,47,48,49,50,52,53,55,56,57,58,64,67,68,69,70,71,72,73,74,],[30,-9,-7,-8,64,-37,-34,-33,-35,-36,-18,-19,-24,-23,-25,-26,-27,-28,-29,-30,-31,-32,-21,-22,-20,]),'OR':([16,41,52,53,55,56,57,58,72,73,74,],[31,31,31,31,-24,-23,-25,-26,-21,-22,-20,]),'AND':([16,41,52,53,55,56,57,58,72,73,74,],[32,32,32,32,-24,-23,-25,-26,-21,-22,-20,]),'GTE':([17,48,54,],[36,36,36,]),'GT':([17,48,54,],[37,37,37,]),'LT':([17,48,54,],[38,38,38,]),'LTE':([17,48,54,],[39,39,39,]),'NEQ':([17,48,54,],[40,40,40,]),'COMMA':([19,20,22,23,24,25,29,42,44,45,46,47,48,49,50,59,60,61,62,63,64,67,68,69,70,71,],[-44,43,-43,-45,-46,-47,-9,-7,-8,65,-37,-34,-33,-35,-36,-38,-39,-40,-41,-42,-27,-28,-29,-30,-31,-32,]),'NUMBER':([26,33,34,35,36,37,38,39,40,65,66,],[47,54,57,-12,-13,-14,-15,-16,-17,68,73,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'line':([0,],[1,]),'rule':([0,1,],[2,4,]),'expr_list':([5,],[7,]),'expr':([5,12,13,15,26,43,65,],[9,25,27,29,49,63,70,]),'condition':([5,12,13,15,26,43,65,],[10,10,10,10,10,10,10,]),'cond_expr_list':([11,18,26,31,32,],[16,41,16,52,53,]),'arg_list':([12,],[20,]),'empty':([12,],[21,]),'array':([12,26,43,65,],[24,50,62,71,]),'cmp':([17,48,54,],[34,34,66,]),'array_elm':([26,],[45,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> line","S'",1,None,None,None),
  ('line -> line rule','line',2,'p_line','parse.py',90),
  ('line -> rule','line',1,'p_line','parse.py',91),
  ('rule -> NAME EQUEL expr_list','rule',3,'p_rule','parse.py',100),
  ('rule -> NAME EQUEL SAME LPAREN NAME RPAREN','rule',6,'p_rule','parse.py',101),
  ('expr_list -> expr_list SEMI expr','expr_list',3,'p_expr_list','parse.py',109),
  ('expr_list -> expr','expr_list',1,'p_expr_list','parse.py',110),
  ('expr -> NAME LPAREN arg_list RPAREN','expr',4,'p_expr','parse.py',118),
  ('expr -> NAME LPAREN empty RPAREN','expr',4,'p_expr','parse.py',119),
  ('expr -> condition IFTHEN expr','expr',3,'p_expr','parse.py',120),
  ('empty -> <empty>','empty',0,'p_empty','parse.py',130),
  ('condition -> LBRACK cond_expr_list RBRACK','condition',3,'p_condition','parse.py',132),
  ('cmp -> EQUEL','cmp',1,'p_cmp','parse.py',135),
  ('cmp -> GTE','cmp',1,'p_cmp','parse.py',136),
  ('cmp -> GT','cmp',1,'p_cmp','parse.py',137),
  ('cmp -> LT','cmp',1,'p_cmp','parse.py',138),
  ('cmp -> LTE','cmp',1,'p_cmp','parse.py',139),
  ('cmp -> NEQ','cmp',1,'p_cmp','parse.py',140),
  ('cond_expr_list -> cond_expr_list OR cond_expr_list','cond_expr_list',3,'p_cond_expr_list','parse.py',144),
  ('cond_expr_list -> cond_expr_list AND cond_expr_list','cond_expr_list',3,'p_cond_expr_list','parse.py',145),
  ('cond_expr_list -> NAME AT NUMBER cmp STRING','cond_expr_list',5,'p_cond_expr_list','parse.py',146),
  ('cond_expr_list -> NAME AT NUMBER cmp NAME','cond_expr_list',5,'p_cond_expr_list','parse.py',147),
  ('cond_expr_list -> NAME AT NUMBER cmp NUMBER','cond_expr_list',5,'p_cond_expr_list','parse.py',148),
  ('cond_expr_list -> NAME cmp STRING','cond_expr_list',3,'p_cond_expr_list','parse.py',149),
  ('cond_expr_list -> NAME cmp NAME','cond_expr_list',3,'p_cond_expr_list','parse.py',150),
  ('cond_expr_list -> NAME cmp NUMBER','cond_expr_list',3,'p_cond_expr_list','parse.py',151),
  ('cond_expr_list -> LPAREN cond_expr_list RPAREN','cond_expr_list',3,'p_cond_expr_list_group','parse.py',165),
  ('array -> LBRACK array_elm RBRACK','array',3,'p_array','parse.py',169),
  ('array_elm -> array_elm COMMA STRING','array_elm',3,'p_array_elm','parse.py',172),
  ('array_elm -> array_elm COMMA NUMBER','array_elm',3,'p_array_elm','parse.py',173),
  ('array_elm -> array_elm COMMA NAME','array_elm',3,'p_array_elm','parse.py',174),
  ('array_elm -> array_elm COMMA expr','array_elm',3,'p_array_elm','parse.py',175),
  ('array_elm -> array_elm COMMA array','array_elm',3,'p_array_elm','parse.py',176),
  ('array_elm -> NAME','array_elm',1,'p_array_elm','parse.py',177),
  ('array_elm -> NUMBER','array_elm',1,'p_array_elm','parse.py',178),
  ('array_elm -> expr','array_elm',1,'p_array_elm','parse.py',179),
  ('array_elm -> array','array_elm',1,'p_array_elm','parse.py',180),
  ('array_elm -> STRING','array_elm',1,'p_array_elm','parse.py',181),
  ('arg_list -> arg_list COMMA STRING','arg_list',3,'p_arg_list','parse.py',190),
  ('arg_list -> arg_list COMMA NAME','arg_list',3,'p_arg_list','parse.py',191),
  ('arg_list -> arg_list COMMA AT','arg_list',3,'p_arg_list','parse.py',192),
  ('arg_list -> arg_list COMMA array','arg_list',3,'p_arg_list','parse.py',193),
  ('arg_list -> arg_list COMMA expr','arg_list',3,'p_arg_list','parse.py',194),
  ('arg_list -> STRING','arg_list',1,'p_arg_list','parse.py',195),
  ('arg_list -> NAME','arg_list',1,'p_arg_list','parse.py',196),
  ('arg_list -> AT','arg_list',1,'p_arg_list','parse.py',197),
  ('arg_list -> array','arg_list',1,'p_arg_list','parse.py',198),
  ('arg_list -> expr','arg_list',1,'p_arg_list','parse.py',199),
]
