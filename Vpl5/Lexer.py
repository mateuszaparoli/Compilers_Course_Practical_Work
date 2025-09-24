import sys
import enum

class Token:
    """
    This class contains the definition of Tokens. A token has two fields: its
    text and its kind. The "kind" of a token is a constant that identifies it
    uniquely. See the TokenType to know the possible identifiers (if you want).
    You don't need to change this class.
    """
    def __init__(self, tokenText, tokenKind):
        # The token's actual text. Used for identifiers, strings, and numbers.
        self.text = tokenText
        # The TokenType that this token is classified as.
        self.kind = tokenKind


class TokenType(enum.Enum):
    """
    These are the possible tokens. You don't need to change this class at all.
    """
    EOF = -1  # End of file
    NLN = 0   # New line
    WSP = 1   # White Space
    COM = 2   # Comment
    NUM = 3   # Number (integers)
    STR = 4   # Strings
    TRU = 5   # The constant true
    FLS = 6   # The constant false
    VAR = 7   # An identifier
    LET = 8   # The 'let' of the let expression
    INX = 9   # The 'in' of the let expression
    END = 10  # The 'end' of the let expression
    EQL = 201
    ADD = 202
    SUB = 203
    MUL = 204
    DIV = 205
    LEQ = 206
    LTH = 207
    NEG = 208
    NOT = 209
    LPR = 210
    RPR = 211
    ASN = 212 # The assignment '<-' operator


class Lexer:
    
    def __init__(self, source):
        """
        The constructor of the lexer. It receives the string that shall be
        scanned.
        TODO: You will need to implement this method.
        """
        self.source = source
        self.position = 0
        self.length = len(source)

    def tokens(self):
        """
        This method is a token generator: it converts the string encapsulated
        into this object into a sequence of Tokens. Examples:

        >>> l = Lexer("1 + 3")
        >>> [tk.kind for tk in l.tokens()]
        [<TokenType.NUM: 3>, <TokenType.ADD: 202>, <TokenType.NUM: 3>]

        >>> l = Lexer('1 * 2 -- 3\\n')
        >>> [tk.kind for tk in l.tokens()]
        [<TokenType.NUM: 3>, <TokenType.MUL: 204>, <TokenType.NUM: 3>]

        >>> l = Lexer("1 + var")
        >>> [tk.kind for tk in l.tokens()]
        [<TokenType.NUM: 3>, <TokenType.ADD: 202>, <TokenType.VAR: 7>]

        >>> l = Lexer("let v <- 2 in v end")
        >>> [tk.kind.name for tk in l.tokens()]
        ['LET', 'VAR', 'ASN', 'NUM', 'INX', 'VAR', 'END']
        """
        token = self.getToken()
        while token.kind != TokenType.EOF:
            if token.kind != TokenType.WSP and token.kind != TokenType.NLN:
                yield token
            token = self.getToken()

    def getToken(self):
        """
        Return the next token.
        TODO: Implement this method!
        """

        if self.position >= self.length:
            return Token("", TokenType.EOF)
         
        current_char = self.source[self.position]
        self.position += 1

        if current_char.isdigit():
            number_text = current_char
            while(self.position < self.length and self.source[self.position].isalnum()):
                number_text += self.source[self.position]
                self.position += 1
            if len(number_text) == 1:
                return Token(number_text, TokenType.NUM)
            elif  number_text[1] == 'b' or number_text[1] == 'B':
                return Token(number_text, TokenType.BIN)
            elif number_text[1] == 'x' or number_text[1] == 'X':
                return Token(number_text, TokenType.HEX)
            elif number_text[0] == '0':
                return Token(number_text, TokenType.OCT)
            else:
                return Token(number_text, TokenType.NUM)
        elif current_char == "\n":
            return Token(current_char, TokenType.NLN)
        elif current_char == " ":
            return Token(current_char, TokenType.WSP)
        elif current_char == "-":
            if self.position < self.length and self.source[self.position] == '-':
                comment_text = "--"
                while (self.position < self.length and self.source[self.position] != "\n"):
                    comment_text += self.source[self.position]
                    self.position += 1
                return Token(comment_text, TokenType.COM)
            return Token(current_char, TokenType.SUB)
        
        elif current_char == "=":
            return Token(current_char, TokenType.EQL)
        elif current_char == "+":
            return Token(current_char, TokenType.ADD)
        elif current_char == "*":
            return Token(current_char, TokenType.MUL)
        elif current_char == "/":
            return Token(current_char, TokenType.DIV)
        elif current_char == "<":
            if self.position < self.length and self.source[self.position] == '-':
                self.position += 1
                return Token("<-", TokenType.ASN)
            elif self.position < self.length and self.source[self.position] == '=':
                self.position += 1
                return Token("<=", TokenType.LEQ)
            else:
                return Token(current_char, TokenType.LTH)
        elif current_char == "~":
            return Token(current_char, TokenType.NEG)
        elif current_char == 'n':
            if self.source[self.position] == 'o' and self.source[self.position + 1] == 't':
                self.position += 2 
                return Token("not", TokenType.NOT)
        elif current_char == "(":
            if self.position < self.length and self.source[self.position] != "*":
                return Token(current_char, TokenType.LPR)
            else:
                comment_text = "(*"
                self.position +=1
                while (self.source[self.position:self.position+2] != "*)"):
                    comment_text += self.source[self.position]
                    self.position += 1
                comment_text += "*)"
                self.position +=2
                return Token(comment_text, TokenType.COM)
        elif current_char == ")":
            return Token(current_char, TokenType.RPR)
        elif current_char == "t":
            if self.source[self.position] == 'r' and self.source[self.position + 1] == 'u' and self.source[self.position + 2] == 'e':
                self.position += 3
                return Token('true', TokenType.TRU)
        elif current_char == "f":
            if self.source[self.position] == 'a' and self.source[self.position + 1] == 'l' and self.source[self.position + 2] == 's' and self.source[self.position + 3] == 'e':
                self.position += 4
                return Token('true', TokenType.FLS)
        elif current_char.isalpha():
            identifier_text = current_char
            while(self.position < self.length and self.source[self.position].isalnum()):
                identifier_text += self.source[self.position]
                self.position += 1
            if identifier_text == "let":
                return Token(identifier_text, TokenType.LET)
            elif identifier_text == "in":
                return Token(identifier_text, TokenType.INX)
            elif identifier_text == "end":
                return Token(identifier_text, TokenType.END)
            else:
                return Token(identifier_text, TokenType.VAR)
        else:
            raise ValueError(f"Unexpected character: {current_char}")