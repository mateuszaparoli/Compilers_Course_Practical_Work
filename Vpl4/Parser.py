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
        >>> parser = Parser([Token('123', TokenType.INT)])
        >>> exp = parser.parse()
        >>> exp.eval()
        123

        
        >>> parser = Parser([Token('True', TokenType.TRU)])
        >>> exp = parser.parse()
        >>> exp.eval()
        True

        >>> parser = Parser([Token('False', TokenType.FLS)])
        >>> exp = parser.parse()
        >>> exp.eval()
        False

        >>> tk0 = Token('~', TokenType.NEG)
        >>> tk1 = Token('123', TokenType.INT)
        >>> parser = Parser([tk0, tk1])
        >>> exp = parser.parse()
        >>> exp.eval()
        -123

        >>> tk0 = Token('3', TokenType.INT)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        12

        >>> tk0 = Token('3', TokenType.INT)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('~', TokenType.NEG)
        >>> tk3 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> exp.eval()
        -12

        >>> tk0 = Token('30', TokenType.INT)
        >>> tk1 = Token('/', TokenType.DIV)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        7

        >>> tk0 = Token('3', TokenType.INT)
        >>> tk1 = Token('+', TokenType.ADD)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        7

        >>> tk0 = Token('30', TokenType.INT)
        >>> tk1 = Token('-', TokenType.SUB)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        26

        >>> tk0 = Token('2', TokenType.INT)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('(', TokenType.LPR)
        >>> tk3 = Token('3', TokenType.INT)
        >>> tk4 = Token('+', TokenType.ADD)
        >>> tk5 = Token('4', TokenType.INT)
        >>> tk6 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> exp.eval()
        14

        >>> tk0 = Token('4', TokenType.INT)
        >>> tk1 = Token('==', TokenType.EQL)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        True

        >>> tk0 = Token('4', TokenType.INT)
        >>> tk1 = Token('<=', TokenType.LEQ)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        True

        >>> tk0 = Token('4', TokenType.INT)
        >>> tk1 = Token('<', TokenType.LTH)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> exp.eval()
        False

        >>> tk0 = Token('not', TokenType.NOT)
        >>> tk1 = Token('4', TokenType.INT)
        >>> tk2 = Token('<', TokenType.LTH)
        >>> tk3 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> exp.eval()
        True
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
        return self.not_expr()
    
    def not_expr(self):
        token = self.current_token()
        if token and token.kind.name == 'NOT':
            self.eat()
            exp = self.not_expr()
            return Not(exp)
        else:
            return self.comparison_expr()
 
 
    def comparison_expr(self):
        left = self.additive_expr()
        return self.comparison_rest(left)

    def comparison_rest(self, left):
        token = self.current_token()
        
        if token and token.kind.name == 'EQL':
            self.eat()
            right = self.additive_expr()
            return self.comparison_rest(Eql(left, right))
        elif token and token.kind.name == 'LEQ':
            self.eat()
            right = self.additive_expr()
            return self.comparison_rest(Leq(left, right))
        elif token and token.kind.name == 'LTH':
            self.eat()
            right = self.additive_expr()
            return self.comparison_rest(Lth(left, right))
        
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
        if token and token.kind.name == 'NEG':
            self.eat()
            exp = self.unary_expr()
            return Neg(exp)
        return self.primary()

    def primary(self):
        token = self.current_token()
        
        if token.kind.name == 'LPR':
            self.eat()
            exp = self.expression()
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
            raise ValueError(f"Unexpected token: {token.kind.name}")