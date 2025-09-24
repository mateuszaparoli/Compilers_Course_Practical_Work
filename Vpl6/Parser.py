from ast import If
import sys

from Expression import *
from Lexer import Token, TokenType

"""
This file implements the parser of arithmetic expressions.

References:
    see https://www.engr.mun.ca/~theo/Misc/exp_parsing.htm
"""

class Parser:
    def __init__(self, tokens):
        """
        Initializes the parser. The parser keeps track of the list of tokens
        and the current token. For instance:
        """
        self.tokens = list(tokens)
        self.cur_token_idx = 0

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
        >>> tk1 = Token('/', TokenType.DIV)
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
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('<-', TokenType.ASN)
        >>> tk3 = Token('42', TokenType.NUM)
        >>> tk4 = Token('in', TokenType.INX)
        >>> tk5 = Token('v', TokenType.VAR)
        >>> tk6 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        42

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('<-', TokenType.ASN)
        >>> tk3 = Token('21', TokenType.NUM)
        >>> tk4 = Token('in', TokenType.INX)
        >>> tk5 = Token('v', TokenType.VAR)
        >>> tk6 = Token('+', TokenType.ADD)
        >>> tk7 = Token('v', TokenType.VAR)
        >>> tk8 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7, tk8])
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

    def expression(self):
        return self.if_else_expr()

    def if_else_expr(self):
        token = self.current_token()
        if token and token.kind.name == 'IFX':
            self.eat()
            cond = self.or_expr()
            if self.current_token() and self.current_token().kind.name == 'THN':
                self.eat()
                then = self.or_expr()
                if self.current_token() and self.current_token().kind.name == 'ELS':
                    self.eat()
                    els = self.or_expr()
                    return self.if_else_expr(IfThenElse(cond, then, els))
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
        
        return left

    def unary_expr(self):
        token = self.current_token()
        if token and token.kind.name == 'LET':
            self.eat()
            var_token = self.current_token()
            var_name = var_token.text
            self.eat()
            asn_token = self.current_token()
            self.eat()
            value_expr = self.expression()
            in_token = self.current_token()
            self.eat()
            body_expr = self.expression()
            end_token = self.current_token()
            self.eat()
            return Let(var_name, value_expr, body_expr)
        elif token and token.kind.name == 'NEG':
            self.eat()
            exp = self.unary_expr()
            return Neg(exp)
        elif token and token.kind.name == 'NOT':
            self.eat()
            exp = self.unary_expr()
            return Not(exp)
        return self.primary()

    def primary(self):
        token = self.current_token()
        
        if token.kind.name == 'LPR':
            self.eat()
            exp = self.expression()
            if self.current_token() and self.current_token().kind.name == 'RPR':
                self.eat()
                return exp
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