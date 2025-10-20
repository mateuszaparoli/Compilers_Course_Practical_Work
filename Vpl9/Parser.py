import sys

from Expression import *
from Lexer import Token, TokenType

"""
This file implements a parser for SML with anonymous functions. The grammar is
as follows:

fn_exp  ::= fn <var> => fn_exp
          | if_exp
if_exp  ::= <if> if_exp <then> fn_exp <else> fn_exp
          | or_exp
or_exp  ::= and_exp (or and_exp)*
and_exp ::= eq_exp (and eq_exp)*
eq_exp  ::= cmp_exp (= cmp_exp)*
cmp_exp ::= add_exp ([<=|<] add_exp)*
add_exp ::= mul_exp ([+|-] mul_exp)*
mul_exp ::= uny_exp ([*|div|mod] uny_exp)*
uny_exp ::= <not> uny_exp
          | ~ uny_exp
          | let_exp
let_exp ::= <let> decl <in> fn_exp <end>
          | val_exp
val_exp ::= val_tk (val_tk)*
val_tk  ::= <var> | ( fn_exp ) | <num> | <true> | <false>

decl    ::= val <var> = fn_exp
          | fun <var> <var> = fn_exp

References:
    see https://www.engr.mun.ca/~theo/Misc/exp_parsing.htm#classic
"""

class Parser:
    def __init__(self, tokens):
        """
        Initializes the parser. The parser keeps track of the list of tokens
        and the current token. For instance:
        """
        self.tokens = list(tokens)
        self.cur_token_idx = 0 # This is just a suggestion!
        # TODO: you might want to implement more stuff in the initializer :)

    def parse(self):
        """
        Returns the expression associated with the stream of tokens.

        Examples:
        >>> parser = Parser([Token('123', TokenType.NUM)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        123

        >>> parser = Parser([Token('True', TokenType.TRU)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> parser = Parser([Token('False', TokenType.FLS)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('~', TokenType.NEG)
        >>> tk1 = Token('123', TokenType.NUM)
        >>> parser = Parser([tk0, tk1])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        -123

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        12

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('~', TokenType.NEG)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        -12

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('div', TokenType.DIV)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        7

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('+', TokenType.ADD)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        7

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('-', TokenType.SUB)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        26

        >>> tk0 = Token('2', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('(', TokenType.LPR)
        >>> tk3 = Token('3', TokenType.NUM)
        >>> tk4 = Token('+', TokenType.ADD)
        >>> tk5 = Token('4', TokenType.NUM)
        >>> tk6 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        14

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('==', TokenType.EQL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<=', TokenType.LEQ)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<', TokenType.LTH)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('not', TokenType.NOT)
        >>> tk1 = Token('(', TokenType.LPR)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> tk3 = Token('<', TokenType.LTH)
        >>> tk4 = Token('4', TokenType.NUM)
        >>> tk5 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('true', TokenType.TRU)
        >>> tk1 = Token('or', TokenType.ORX)
        >>> tk2 = Token('false', TokenType.FLS)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('true', TokenType.TRU)
        >>> tk1 = Token('and', TokenType.AND)
        >>> tk2 = Token('false', TokenType.FLS)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('val', TokenType.VAL)
        >>> tk2 = Token('v', TokenType.VAR)
        >>> tk3 = Token('=', TokenType.EQL)
        >>> tk4 = Token('42', TokenType.NUM)
        >>> tk5 = Token('in', TokenType.INX)
        >>> tk6 = Token('v', TokenType.VAR)
        >>> tk7 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        42

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('val', TokenType.VAL)
        >>> tk2 = Token('v', TokenType.VAR)
        >>> tk3 = Token('=', TokenType.EQL)
        >>> tk4 = Token('21', TokenType.NUM)
        >>> tk5 = Token('in', TokenType.INX)
        >>> tk6 = Token('v', TokenType.VAR)
        >>> tk7 = Token('+', TokenType.ADD)
        >>> tk8 = Token('v', TokenType.VAR)
        >>> tk9 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7, tk8, tk9])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        42

        >>> tk0 = Token('if', TokenType.IFX)
        >>> tk1 = Token('2', TokenType.NUM)
        >>> tk2 = Token('<', TokenType.LTH)
        >>> tk3 = Token('3', TokenType.NUM)
        >>> tk4 = Token('then', TokenType.THN)
        >>> tk5 = Token('1', TokenType.NUM)
        >>> tk6 = Token('else', TokenType.ELS)
        >>> tk7 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        1

        >>> tk0 = Token('if', TokenType.IFX)
        >>> tk1 = Token('false', TokenType.FLS)
        >>> tk2 = Token('then', TokenType.THN)
        >>> tk3 = Token('1', TokenType.NUM)
        >>> tk4 = Token('else', TokenType.ELS)
        >>> tk5 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        2

        >>> tk0 = Token('fn', TokenType.FNX)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('=>', TokenType.ARW)
        >>> tk3 = Token('v', TokenType.VAR)
        >>> tk4 = Token('+', TokenType.ADD)
        >>> tk5 = Token('1', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> print(exp.accept(ev, None))
        Fn(v)

        >>> tk0 = Token('(', TokenType.LPR)
        >>> tk1 = Token('fn', TokenType.FNX)
        >>> tk2 = Token('v', TokenType.VAR)
        >>> tk3 = Token('=>', TokenType.ARW)
        >>> tk4 = Token('v', TokenType.VAR)
        >>> tk5 = Token('+', TokenType.ADD)
        >>> tk6 = Token('1', TokenType.NUM)
        >>> tk7 = Token(')', TokenType.RPR)
        >>> tk8 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7, tk8])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        3

        >>> t0 = Token('let', TokenType.LET)
        >>> t1 = Token('fun', TokenType.FUN)
        >>> t2 = Token('f', TokenType.VAR)
        >>> t3 = Token('v', TokenType.VAR)
        >>> t4 = Token('=', TokenType.EQL)
        >>> t5 = Token('v', TokenType.VAR)
        >>> t6 = Token('+', TokenType.ADD)
        >>> t7 = Token('v', TokenType.VAR)
        >>> t8 = Token('in', TokenType.INX)
        >>> t9 = Token('f', TokenType.VAR)
        >>> tA = Token('2', TokenType.NUM)
        >>> tB = Token('end', TokenType.END)
        >>> parser = Parser([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, tA, tB])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        4
        """
        exp = self.expression()
        return exp

    def current_token(self):
        if self.cur_token_idx >= len(self.tokens):
            return None
        return self.tokens[self.cur_token_idx]

    def eat(self):
        if self.cur_token_idx < len(self.tokens):
            self.cur_token_idx += 1

    def fn_expr(self):
        """Parse: fn <var> => fn_exp | if_exp"""
        token = self.current_token()
        if token and token.kind.name == 'FNX':
            self.eat()
            param_token = self.current_token()
            if not param_token or param_token.kind.name != 'VAR':
                sys.exit("Parse error: expected variable after 'fn'")
            param_name = param_token.text
            self.eat()
            # Expect '=>'
            arrow_token = self.current_token()
            if not arrow_token or arrow_token.kind.name != 'ARW':
                sys.exit("Parse error: expected '=>' after parameter")
            self.eat()
            body = self.fn_expr()
            return Fn(param_name, body)
        return self.if_else_expr()

    def expression(self):
        return self.fn_expr()

    def if_else_expr(self):
        token = self.current_token()
        if token and token.kind.name == 'IFX':
            self.eat()
            cond = self.if_else_expr()
            if self.current_token() and self.current_token().kind.name == 'THN':
                self.eat()
                then = self.fn_expr()
                if self.current_token() and self.current_token().kind.name == 'ELS':
                    self.eat()
                    els = self.fn_expr()
                    return IfThenElse(cond, then, els)
        return self.or_expr()
         
    def or_expr(self):
        left = self.and_expr()
        return self.or_rest(left)
    
    def or_rest(self,left):
        token = self.current_token()

        if token and token.kind.name == 'ORX':
            self.eat()
            right = self.and_expr()
            return self.or_rest(Or(left, right))
        return left
    
    def and_expr(self):
        left = self.comparison_expr()
        return self.and_rest(left)

    def and_rest(self,left):
        token = self.current_token()

        if token and token.kind.name == 'AND':
            self.eat()
            right = self.comparison_expr()
            return self.and_rest(And(left, right))
        return left        

    def comparison_expr(self):  
        left = self.less_expr()
        return self.comparison_rest(left)

    def comparison_rest(self, left):
        token = self.current_token()
        
        if token and token.kind.name == 'EQL':
            self.eat()
            right = self.less_expr()
            return self.comparison_rest(Eql(left, right))
        return left

    def less_expr(self):
        left = self.additive_expr()
        return self.less_rest(left)
    
    def less_rest(self, left):
        token = self.current_token()
        
        if token and token.kind.name == 'LEQ':
            self.eat()
            right = self.additive_expr()
            return self.less_rest(Leq(left, right))
        elif token and token.kind.name == 'LTH':
            self.eat()
            right = self.additive_expr()
            return self.less_rest(Lth(left, right))
        return left

    def additive_expr(self):
        left = self.multiplicative_expr()
        return self.additive_rest(left)

    def additive_rest(self, left):
        token = self.current_token()
        
        if token and token.kind.name == 'ADD':
            self.eat()
            right = self.multiplicative_expr()
            return self.additive_rest(Add(left, right))
        elif token and token.kind.name == 'SUB':
            self.eat()
            right = self.multiplicative_expr()
            return self.additive_rest(Sub(left, right))
        
        return left

    def multiplicative_expr(self):
        left = self.unary_expr()
        return self.multiplicative_rest(left)

    def multiplicative_rest(self, left):
        token = self.current_token()
        
        if token and token.kind.name == 'MUL':
            self.eat()
            right = self.unary_expr()
            return self.multiplicative_rest(Mul(left, right))
        elif token and token.kind.name == 'DIV':
            self.eat()
            right = self.unary_expr()
            return self.multiplicative_rest(Div(left, right))
        elif token and token.kind.name == 'MOD':
            self.eat()
            right = self.unary_expr()
            return self.multiplicative_rest(Mod(left, right))
        
        return left

    def unary_expr(self):
        token = self.current_token()
        if token and token.kind.name == 'NEG':
            self.eat()
            exp = self.unary_expr()
            return Neg(exp)
        elif token and token.kind.name == 'NOT':
            self.eat()
            exp = self.unary_expr()
            return Not(exp)
        return self.let_expr()

    def let_expr(self):
        token = self.current_token()
        if token and token.kind.name == 'LET':
            self.eat()
            decl_token = self.current_token()
            if not decl_token:
                sys.exit("Parse error")
            
            if decl_token.kind.name == 'VAL':
                self.eat()
                var_token = self.current_token()
                if not var_token or var_token.kind.name != 'VAR':
                    sys.exit("Parse error")
                var_name = var_token.text
                self.eat()
                
                eql_token = self.current_token()
                if not eql_token or eql_token.kind.name != 'EQL':
                    sys.exit("Parse error")
                self.eat()
                
                value_expr = self.fn_expr()
                
                in_token = self.current_token()
                if not in_token or in_token.kind.name != 'INX':
                    sys.exit("Parse error")
                self.eat()
                
                body_expr = self.fn_expr()
                
                end_token = self.current_token()
                if not end_token or end_token.kind.name != 'END':
                    sys.exit("Parse error")
                self.eat()
                
                return Let(var_name, value_expr, body_expr)
            
            elif decl_token.kind.name == 'FUN':
                self.eat()
                fun_name_token = self.current_token()
                if not fun_name_token or fun_name_token.kind.name != 'VAR':
                    sys.exit("Parse error")
                fun_name = fun_name_token.text
                self.eat()
                
                param_token = self.current_token()
                if not param_token or param_token.kind.name != 'VAR':
                    sys.exit("Parse error")
                param_name = param_token.text
                self.eat()
                
                eql_token = self.current_token()
                if not eql_token or eql_token.kind.name != 'EQL':
                    sys.exit("Parse error")
                self.eat()
                
                body_expr = self.fn_expr()
                
                in_token = self.current_token()
                if not in_token or in_token.kind.name != 'INX':
                    sys.exit("Parse error")
                self.eat()
                
                let_body_expr = self.fn_expr()
                
                end_token = self.current_token()
                if not end_token or end_token.kind.name != 'END':
                    sys.exit("Parse error")
                self.eat()
                
                fun_expr = Fun(fun_name, param_name, body_expr)
                return Let(fun_name, fun_expr, let_body_expr)
            else:
                sys.exit("Parse error")
        
        return self.val_expr()

    def val_expr(self):
        left = self.val_tk()
        
        while True:
            token = self.current_token()
            if token and (token.kind.name == 'VAR' or 
                         token.kind.name == 'LPR' or 
                         token.kind.name == 'NUM' or 
                         token.kind.name == 'TRU' or 
                         token.kind.name == 'FLS'):
                right = self.val_tk()
                left = App(left, right)
            else:
                break
        
        return left

    def val_tk(self):
        token = self.current_token()
        
        if not token:
            sys.exit("Parse error")
        
        if token.kind.name == 'LPR':
            self.eat()
            exp = self.fn_expr()
            if self.current_token() and self.current_token().kind.name == 'RPR':
                self.eat()
                return exp
            else:
                sys.exit("Parse error")
        elif token.kind.name == 'NUM':
            self.eat()
            return Num(int(token.text))
        elif token.kind.name == 'TRU':
            self.eat()
            return Bln(True)
        elif token.kind.name == 'FLS':
            self.eat()
            return Bln(False)
        elif token.kind.name == 'VAR':
            self.eat()
            return Var(token.text)
        else:
            sys.exit(f"Parse error")

    def primary(self):
        token = self.current_token()
        
        if token.kind.name == 'LPR':
            self.eat()
            exp = self.expression()
            if self.current_token() and self.current_token().kind.name == 'RPR':
                self.eat()
                return exp
        elif token and token.kind.name == 'IFX':
            return self.if_else_expr()
        elif token.kind.name == 'NUM':
            self.eat()
            return Num(int(token.text))
        elif token.kind.name == 'TRU':
            self.eat()
            return Bln(True)
        elif token.kind.name == 'FLS':
            self.eat()
            return Bln(False)
        elif token.kind.name == 'VAR':
            self.eat()
            return Var(token.text)
        else:
            sys.exit("Parse error")