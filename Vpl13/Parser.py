import sys

from Expression import *
from Lexer import Token, TokenType

"""
Precedence table:
    1: not ~ ()
    2: *   /
    3: +   -
    4: <   <=   >=   >
    5: =
    6: and
    7: or
    8: if-then-else

Notice that not 2 < 3 must be a type error, as we are trying to apply a boolean
operation (not) onto a number. However, in assembly code this program works,
because not 2 is 0. The bottom line is: don't worry about programs like this
one: the would have been ruled out by type verification anyway.

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
        self.tokens.append(Token("", TokenType.EOF))
        self.cur_token_idx = 0 # This is just a suggestion!
        # You can (and probably should!) modify this method. Ok!

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
            return IfThenElse(cond, e0, e1)
        return self._parse_or()

    def _parse_and(self):
        left = self._parse_equality()
        while self._current().kind == TokenType.AND:
            self._advance()
            right = self._parse_equality()
            left = And(left, right)
        return left

    def _parse_or(self):
        left = self._parse_and()
        while self._current().kind == TokenType.ORX:
            self._advance()
            right = self._parse_and()
            left = Or(left, right)
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

    def _parse_additive(self):
        left = self._parse_multiplicative()
        while True:
            token_kind = self._current().kind
            if token_kind == TokenType.ADD:
                self._advance()
                right = self._parse_multiplicative()
                left = Add(left, right)
            elif token_kind == TokenType.SUB:
                self._advance()
                right = self._parse_multiplicative()
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
            # Unary minus cannot be immediately followed by an 'if' expression
            if self._current().kind == TokenType.IFX:
                self._error("")
            return Neg(self._parse_unary())
        if token_kind == TokenType.NOT:
            self._advance()
            if self._current().kind == TokenType.IFX:
                self._error("")
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
        if token.kind == TokenType.IFX:
            # allow nested 'if' expressions in primary position
            self._advance()
            cond = self._parse_or()
            self._expect(TokenType.THN)
            e0 = self._parse_expression()
            self._expect(TokenType.ELS)
            e1 = self._parse_expression()
            return IfThenElse(cond, e0, e1)
        self._error("")

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