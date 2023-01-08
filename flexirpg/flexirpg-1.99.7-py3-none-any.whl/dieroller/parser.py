# Dice roll parser.
#
# Copyright (C) 2009-2011 David Vrabel
#
import ply.lex as lex
import ply.yacc as yacc
import random
import sys

from orpg.lib.text import html_to_text

class symtab_default(object):
    def lookup(self, var):
        return None

    def format_error(self, err):
        return err

class dice_roll_type_error(Exception):
    pass

class dice_roll_result(object):
    NUM = 0
    DICE = 1
    STRING = 2

    def __init__(self, rtype, value, text):
        self.__rtype = rtype
        self.__value = value
        self.__text  = text

    def __get_rtype(self):
        return self.__rtype
    def __get_value(self):
        if self.__value == None:
            raise dice_roll_type_error()
        return self.__value
    def __get_text(self):
        return self.__text

    def __set_value(self, v):
        self.__value = v;
    def __set_text(self, t):
        self.__text = t;

    rtype = property(__get_rtype)
    value = property(__get_value, __set_value)
    text  = property(__get_text, __set_text)

    def is_num(self):
        return self.rtype == self.NUM
    def is_dice(self):
        return self.rtype == self.DICE
    def is_string(self):
        return self.rtype == self.STRING

    def quoted_string(self):
        if self.is_string():
            return '"' + self.text + '"'
        else:
            return str(self.value)

    def bare_string(self):
        if self.is_string():
            return html_to_text(self.text)
        else:
            return str(self.value)        

class dice_roll_num(dice_roll_result):
    def __init__(self, value, text):
        dice_roll_result.__init__(self, self.NUM, value, text)

class dice_roll_dice(dice_roll_result):
    MAX_DISPLAYED_ROLLS = 20

    def __init__(self, count, sides):
        dice_roll_result.__init__(self, self.DICE, 0, str(count) + "d" + str(sides))
        self.text += "<i>("
        for i in range(count):
            r = random.randint(1, sides)
            self.value += r
            if i <= self.MAX_DISPLAYED_ROLLS:
                if i > 0:
                    self.text += ","
                if i < self.MAX_DISPLAYED_ROLLS:
                    self.text += str(r)
                else:
                    self.text += "..."
        self.text += ")</i>"

class dice_roll_string(dice_roll_result):
    def __init__(self, text):
        dice_roll_result.__init__(self, self.STRING, None, text)

class dice_roll_error(Exception):
    def __init__(self, symtab, err):
        if symtab:
            self.str = symtab.format_error(err)
        else:
            self.str = err

class dice_roll_lexer:
    tokens = (
        'NUMBER',
        'ASSIGN',
        'PLUS',
        'MINUS',
        'MULT',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'VARIABLE',
        'DICE',
        'EQ',
        'NE',
        'LT',
        'GT',
        'LT_EQ',
        'GT_EQ',
        'AND',
        'OR',
        'NOT',
        'IF',
        'THEN',
        'ELSE',
        'STRING',
        )

    reserved = {
        'd' : 'DICE',
        'and' : 'AND',
        'or' : 'OR',
        'not' : 'NOT',
        'if' : 'IF',
        'then' : 'THEN',
        'else' : 'ELSE',
        }

    t_ASSIGN  = r'='
    t_EQ      = r'=='
    t_NE      = r'!='
    t_LT      = r'<'
    t_GT      = r'>'
    t_LT_EQ   = r'<='
    t_GT_EQ   = r'>='
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_MULT    = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)    
        return t

    def t_VARIABLE(self, t):
        r'[a-zA-Z_]([a-zA-Z_][a-zA-Z0-9_]*)?'
        t.type = self.reserved.get(t.value, 'VARIABLE')
        return t

    def t_STRING(self, t):
        r'\"[^\"]*\"'
        t.value = t.value[1:-1]
        return t

    t_ignore  = ' \t\n\r'

    def t_error(self, t):
        raise dice_roll_error(self.symtab, "invalid character '" + t.value + "'")

    def __init__(self, symtab):
        self.symtab = symtab
        self.lexer = lex.lex(module=self)

class dice_roll_parser:
    tokens = dice_roll_lexer.tokens

    precedence = (
        ('right', 'ASSIGN'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', 'LT', 'GT', 'LT_EQ', 'GT_EQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIVIDE'),
        ('right', 'UMINUS', 'NOT'),
        ('left', 'DICE'),
        )

    def p_dice_roll(self, p):
        '''dice_roll : expression
                     | assignment_expression
                     | if_expression'''
        if p[1].is_string():
            p[0] = dice_roll_string(parse_all_dice_rolls(self.symtab, p[1].text))
        else:
            p[0] = p[1]

    def p_expression_assign(self, p):
        '''assignment_expression : VARIABLE ASSIGN expression
                                 | VARIABLE ASSIGN if_expression'''
        var = p[1]
        expr = self.__lookup(var)
        if p[3].is_string():
            p[3] = dice_roll_string(parse_all_dice_rolls(self.symtab, p[3].text))
        try:
            expr.set_value(p[3])
        except dice_roll_error as e:
            raise dice_roll_error(self.symtab, e.str);
        p[0] = p[3]

    def p_expression_if(self, p):
        'if_expression : IF expression THEN expression ELSE expression'
        cond = p[2]
        if cond.value:
            p[0] = p[4]
        else:
            p[0] = p[6]

    def p_expression_or(self, p):
        'expression : expression OR expression'
        cond = p[1].value or p[3].value
        p[0] = dice_roll_num(int(cond), str(cond))

    def p_expression_and(self, p):
        'expression : expression AND expression'
        cond = p[1].value and p[3].value
        p[0] = dice_roll_num(int(cond), str(cond))

    def p_expression_eq(self, p):
        'expression : expression EQ expression'
        cond = p[1].value == p[3].value
        p[0] = dice_roll_num(int(cond), str(cond))

    def p_expression_ne(self, p):
        'expression : expression NE expression'
        cond = p[1].value != p[3].value
        p[0] = dice_roll_num(int(cond), str(cond))

    def p_expression_lt(self, p):
        'expression : expression LT expression'
        cond = p[1].value < p[3].value
        p[0] = dice_roll_num(int(cond), str(cond))

    def p_expression_gt(self, p):
        'expression : expression GT expression'
        cond = p[1].value > p[3].value
        p[0] = dice_roll_num(int(cond), str(cond))

    def p_expression_lt_eq(self, p):
        'expression : expression LT_EQ expression'
        cond = p[1].value <= p[3].value
        p[0] = dice_roll_num(int(cond), str(cond))

    def p_expression_gt_eq(self, p):
        'expression : expression GT_EQ expression'
        cond = p[1].value >= p[3].value
        p[0] = dice_roll_num(int(cond), str(cond))

    def p_expression_plus(self, p):
        'expression : expression PLUS expression'
        p[0] = dice_roll_num(p[1].value + p[3].value, p[1].text + " + " + p[3].text)

    def p_expression_minus(self, p):
        'expression : expression MINUS expression'
        p[0] = dice_roll_num(p[1].value - p[3].value, p[1].text + " - " + p[3].text)

    def p_expression_mult(self, p):
        'expression : expression MULT expression'
        p[0] = dice_roll_num(p[1].value * p[3].value, p[1].text + " * " + p[3].text)

    def p_expression_div(self, p):
        'expression : expression DIVIDE expression'
        if p[3].value == 0:
            raise dice_roll_error(self.symtab, "division by zero")
        p[0] = dice_roll_num(p[1].value // p[3].value, p[1].text + " / " + p[3].text)

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = dice_roll_num(-p[2].value, "-" + p[2].text)

    def p_expression_not(self, p):
        'expression : NOT expression'
        cond = not p[2].value
        p[0] = dice_roll_num(int(cond), str(cond))

    def p_expression_dice(self, p):
        'expression : expression DICE expression'
        p[0] = dice_roll_dice(p[1].value, p[3].value)

    def p_expression_paren(self, p):
        '''expression : LPAREN expression RPAREN
                      | LPAREN assignment_expression RPAREN
                      | LPAREN if_expression RPAREN'''
        if p[2].is_string():
            p[0] = p[2]
        elif p[2].is_dice():
            p[0] = dice_roll_num(p[2].value, p[2].text)
        else:
            p[0] = dice_roll_num(p[2].value, str(p[2].value))

    def p_expression_num(self, p):
        'expression : NUMBER'
        p[0] = dice_roll_num(p[1], str(p[1]))

    def p_expression_var(self, p):
        'expression : VARIABLE'
        var = p[1]
        expr = self.__lookup(var)
        if expr.evaluating():
            raise dice_roll_error(self.symtab, "circular reference to '" + var + "'")
        result = expr.eval()
        if result.is_num():
            p[0]= dice_roll_num(result.value, str(result.value))
        else:
            p[0] = result

    def p_expression_string(self, p):
        'expression : STRING'
        p[0] = dice_roll_string(p[1])

    def p_error(self, p):
        raise dice_roll_error(self.symtab, "syntax error")

    def __init__(self, symtab = None):
        if not symtab:
            symtab = symtab_default();

        self.symtab = symtab

        self.lexer = dice_roll_lexer(symtab)
        self.parser = yacc.yacc(module=self, tabmodule="dicerolltab", debug=0)

    def parse(self, text):
        try:
            return self.parser.parse(text, lexer=self.lexer.lexer)
        except dice_roll_type_error as e:
            raise dice_roll_error(self.symtab, "type mismatch")

    def __lookup(self, var):
        expr = self.symtab.lookup(var)
        if not expr:
            raise dice_roll_error(self.symtab, "'" + var + "' not found")
        return expr

def parse_all_dice_rolls(symtab, in_str):
    parser = dice_roll_parser(symtab)
    brackets = 0
    out_str = ""
    for i in range(len(in_str)):
        if in_str[i] == "[":
            if brackets == 0:
                start = i
            brackets += 1
        elif in_str[i] == "]":
            if brackets == 1:
                hidden = False
                if in_str[start+1] == '#':
                    start += 1
                    hidden = True
                result = parser.parse(in_str[start+1:i])
                if not hidden:
                    if result.is_string():
                        out_str += result.text
                    else:
                        if str(result.value) == result.text:
                            out_str += "<dice result='%d'>%d</dice>" \
                                % (result.value, result.value)
                        else:
                            out_str += "<dice result='%d'>[%s] = %d</dice>" \
                                % (result.value, result.text, result.value)
            brackets -= 1
        else:
            if brackets == 0:
                out_str += in_str[i]
    if brackets > 0:
        raise dice_roll_error(symtab, "missing ']'")
    return out_str

if __name__ == "__main__":
    # Generatate the parser tables by creating a parser.
    dice_roll_parser(None)
