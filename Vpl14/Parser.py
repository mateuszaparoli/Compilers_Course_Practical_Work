import sys

from Expression import *
from Lexer import Token, TokenType

class Parser:
    def __init__(self, tokens):
        """
        Initializes the parser. The parser keeps track of the list of tokens
        and the current token. For instance:
        """
        self.tokens = list(tokens)
        self.tokens.append(Token("", TokenType.EOF))
        self.cur_token_idx = 0

    def parse(self):
        """
        Returns the expression associated with the stream of tokens.

        Examples:
        >>> parser = Parser([Token('123', TokenType.NUM)])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        123

        >>> parser = Parser([Token('True', TokenType.TRU)])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> parser = Parser([Token('False', TokenType.FLS)])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> tk0 = Token('~', TokenType.NEG)
        >>> tk1 = Token('123', TokenType.NUM)
        >>> parser = Parser([tk0, tk1])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        -123

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        12

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('~', TokenType.NEG)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        -12

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('/', TokenType.DIV)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        7

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('+', TokenType.ADD)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        7

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('-', TokenType.SUB)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        26

        >>> tk0 = Token('2', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('(', TokenType.LPR)
        >>> tk3 = Token('3', TokenType.NUM)
        >>> tk4 = Token('+', TokenType.ADD)
        >>> tk5 = Token('4', TokenType.NUM)
        >>> tk6 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        14

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('==', TokenType.EQL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<=', TokenType.LEQ)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<', TokenType.LTH)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> tk0 = Token('not', TokenType.NOT)
        >>> tk1 = Token('4', TokenType.NUM)
        >>> tk2 = Token('<', TokenType.LTH)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('<-', TokenType.ASN)
        >>> tk3 = Token('42', TokenType.NUM)
        >>> tk4 = Token('in', TokenType.INX)
        >>> tk5 = Token('v', TokenType.VAR)
        >>> tk6 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
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
        >>> g = GenVisitor()
        >>> p = AsmModule.Program({}, [])
        >>> exp = parser.parse()
        >>> v = exp.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        42
        """

        expr = self._parse_expression()
        self._expect(TokenType.EOF)
        return expr

    def _parse_expression(self):
        if self._current().kind == TokenType.IFX:
            self._advance()
            cond = self._parse_or()
            self._expect(TokenType.THN)
            e0 = self._parse_expression()
            self._expect(TokenType.ELS)
            e1 = self._parse_expression()
            self._expect(TokenType.END)
            return IfThenElse(cond, e0, e1)
        if self._current().kind == TokenType.FNX:
            return self._parse_lambda()
        return self._parse_or()

    def _parse_or(self):
        left = self._parse_and()
        while self._current().kind == TokenType.ORX:
            self._advance()
            right = self._parse_and()
            left = Or(left, right)
        return left

    def _parse_and(self):
        left = self._parse_equality()
        while self._current().kind == TokenType.AND:
            self._advance()
            right = self._parse_equality()
            left = And(left, right)
        return left

    def _parse_let(self):
        self._expect(TokenType.LET)
        identifier = self._expect(TokenType.VAR).text
        self._expect(TokenType.ASN)
        exp_def = self._parse_expression()
        self._expect(TokenType.INX)
        exp_body = self._parse_expression()
        self._expect(TokenType.END)
        return Let(identifier, exp_def, exp_body)

    def _parse_lambda(self):
        self._expect(TokenType.FNX)
        formal = self._expect(TokenType.VAR).text
        self._expect(TokenType.ARW)
        body = self._parse_expression()
        return Fn(formal, body)

    def _parse_equality(self):
        left = self._parse_comparison()
        while self._current().kind == TokenType.EQL:
            self._advance()
            right = self._parse_comparison()
            left = Eql(left, right)
        return left

    def _parse_comparison(self):
        left = self._parse_additive()
        while True:
            token_kind = self._current().kind
            if token_kind == TokenType.LEQ:
                self._advance()
                right = self._parse_additive()
                left = Leq(left, right)
            elif token_kind == TokenType.LTH:
                self._advance()
                right = self._parse_additive()
                left = Lth(left, right)
            else:
                break
        return left

    def _parse_application(self):
        left = self._parse_multiplicative()
        while self._is_application_start():
            right = self._parse_multiplicative()
            left = App(left, right)
        return left

    def _is_application_start(self):
        token_kind = self._current().kind
        return token_kind in [TokenType.NUM, TokenType.TRU, TokenType.FLS, 
                             TokenType.VAR, TokenType.LPR, TokenType.LET, TokenType.FNX, 
                             TokenType.NEG, TokenType.NOT]

    def _parse_additive(self):
        left = self._parse_application()
        while True:
            token_kind = self._current().kind
            if token_kind == TokenType.ADD:
                self._advance()
                right = self._parse_application()
                left = Add(left, right)
            elif token_kind == TokenType.SUB:
                self._advance()
                right = self._parse_application()
                left = Sub(left, right)
            else:
                break
        return left

    def _parse_multiplicative(self):
        left = self._parse_unary()
        while True:
            token_kind = self._current().kind
            if token_kind == TokenType.MUL:
                self._advance()
                right = self._parse_unary()
                left = Mul(left, right)
            elif token_kind == TokenType.DIV:
                self._advance()
                right = self._parse_unary()
                left = Div(left, right)
            else:
                break
        return left

    def _parse_unary(self):
        token_kind = self._current().kind
        if token_kind == TokenType.NEG:
            self._advance()
            return Neg(self._parse_unary())
        if token_kind == TokenType.NOT:
            self._advance()
            return Not(self._parse_unary())
        return self._parse_primary()

    def _parse_primary(self):
        token = self._current()
        if token.kind == TokenType.NUM:
            self._advance()
            return Num(int(token.text))
        if token.kind == TokenType.TRU:
            self._advance()
            return Bln(True)
        if token.kind == TokenType.FLS:
            self._advance()
            return Bln(False)
        if token.kind == TokenType.VAR:
            self._advance()
            return Var(token.text)
        if token.kind == TokenType.LPR:
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPR)
            return expr
        if token.kind == TokenType.LET:
            return self._parse_let()
        if token.kind == TokenType.FNX:
            return self._parse_lambda()
        if token.kind == TokenType.IFX:
            return self._parse_expression()
        self._error("Unexpected token")

    def _current(self):
        return self.tokens[self.cur_token_idx]

    def _advance(self):
        if self.cur_token_idx < len(self.tokens) - 1:
            self.cur_token_idx += 1

    def _expect(self, token_type):
        token = self._current()
        if token.kind != token_type:
            self._error(f"Expected {token_type.name}")
        self._advance()
        return token

    def _error(self, message):
        sys.exit(f"Parse error: {message}")