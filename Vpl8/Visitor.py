import sys
from abc import ABC, abstractmethod
from Expression import *

class Visitor(ABC):
    """
    The visitor pattern consists of two abstract classes: the Expression and the
    Visitor. The Expression class defines on method: 'accept(visitor, args)'.
    This method takes in an implementation of a visitor, and the arguments that
    are passed from expression to expression. The Visitor class defines one
    specific method for each subclass of Expression. Each instance of such a
    subclasse will invoke the right visiting method.
    """
    @abstractmethod
    def visit_var(self, exp, arg):
        pass

    @abstractmethod
    def visit_bln(self, exp, arg):
        pass

    @abstractmethod
    def visit_num(self, exp, arg):
        pass

    @abstractmethod
    def visit_eql(self, exp, arg):
        pass

    @abstractmethod
    def visit_add(self, exp, arg):
        pass

    @abstractmethod
    def visit_sub(self, exp, arg):
        pass

    @abstractmethod
    def visit_mul(self, exp, arg):
        pass

    @abstractmethod
    def visit_div(self, exp, arg):
        pass

    @abstractmethod
    def visit_leq(self, exp, arg):
        pass

    @abstractmethod
    def visit_lth(self, exp, arg):
        pass

    @abstractmethod
    def visit_neg(self, exp, arg):
        pass

    @abstractmethod
    def visit_not(self, exp, arg):
        pass

    @abstractmethod
    def visit_let(self, exp, arg):
        pass

    @abstractmethod
    def visit_if(self, exp, arg):
        pass
    
    @abstractmethod
    def visit_or(self, exp, arg):
        pass

    @abstractmethod
    def visit_and(self, exp, arg):
        pass

    @abstractmethod
    def visit_fn(self, exp, arg):
        pass

    @abstractmethod
    def visit_app(self, exp, arg):
        pass

class Function():
    """
    This is the class that represents functions. This class lets us distinguish
    the three types that now exist in the language: numbers, booleans and
    functions. Notice that the evaluation of an expression can now be a
    function. For instance:

        >>> f = Fn('v', Mul(Var('v'), Var('v')))
        >>> ev = EvalVisitor()
        >>> fval = f.accept(ev, {})
        >>> type(fval)
        <class 'Visitor.Function'>
    """
    def __init__(self, formal, body, env):
        self.formal = formal
        self.body = body
        self.env = env
    def __str__(self):
        return f"Fn({self.formal})"

class EvalVisitor(Visitor):
    """
    The EvalVisitor class evaluates logical and arithmetic expressions. The
    result of evaluating an expression is the value of that expression. The
    inherited attribute propagated throughout visits is the environment that
    associates the names of variables with values.

    Examples:
    >>> e0 = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
    >>> e1 = Not(Eql(e0, Num(1764)))
    >>> ev = EvalVisitor()
    >>> e1.accept(ev, {})
    False

    >>> e0 = Let('v', Add(Num(40), Num(2)), Sub(Var('v'), Num(2)))
    >>> e1 = Lth(e0, Var('x'))
    >>> ev = EvalVisitor()
    >>> e1.accept(ev, {'x': 41})
    True
    """
    def visit_var(self, exp, env):
        if exp.identifier in env:
            return env[exp.identifier]
        else:
            sys.exit("Def error")
    
    def visit_bln(self, exp, env):
        return env.get(exp.bln, exp.bln)

    def visit_num(self, exp, env):
        return env.get(exp.num, exp.num)

    def visit_eql(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if (type(left) == type(1) or type(left) == type(True)) and type(right) == type(left):
            return left == right
        else:
            sys.exit("Type error")

    def visit_add(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if type(left) == type(1) and type(right) == type(1):
            return int(left + right)
        else:
            sys.exit("Type error")

    def visit_sub(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if type(left) == type(1) and type(right) == type(1):
            return int(left - right)
        else:
            sys.exit("Type error")
    
    def visit_mul(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if type(left) == type(1) and type(right) == type(1):
            return int(left * right)
        else:
            sys.exit("Type error")

    def visit_div(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if type(left) == type(1) and type(right) == type(1):
            return int(left / right)
        else:
            sys.exit("Type error")

    def visit_leq(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if type(left) == type(1) and type(right) == type(1):
            return left <= right
        else:
            sys.exit("Type error")

    def visit_lth(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if type(left) == type(1) and type(right) == type(1):
            return (left < right)
        else:
            sys.exit("Type error")

    def visit_neg(self, exp, env):
        value = exp.exp.accept(self, env)
        if type(value) == type(1):
            return -value
        else:
            sys.exit("Type error")

    def visit_not(self, exp, env):
        value = exp.exp.accept(self, env)
        if type(value) == type(True):
            return not value
        else:
            sys.exit("Type error")

    def visit_let(self, exp, env):
        value = exp.exp_def.accept(self, env)
        # Aceita int, bool ou Function
        if not (type(value) in [int, bool] or isinstance(value, Function)):
            sys.exit("Type error")
        new_env = env.copy()
        new_env[exp.identifier] = value
        return exp.exp_body.accept(self, new_env)
    
    def visit_if(self, exp, env):
        cond = exp.cond.accept(self, env)
        if type(cond) != type(True):
            sys.exit("Type error")
        else:
            if cond:
                return exp.e0.accept(self, env)
            else:
                return exp.e1.accept(self, env)
        
    def visit_or(self, exp, env):
        left = exp.left.accept(self, env)
        if type(left) != type(True):
            sys.exit("Type error")
        else:
            if left:
                return True
            else:
                right = exp.right.accept(self, env)
                if type(right) != type(True):
                    sys.exit("Type error")
                else:
                    return right

    def visit_and(self, exp, env):
        left = exp.left.accept(self, env)
        if type(left) != type(True):
            sys.exit("Type error")
        if not left:
            return False
        else:
            right = exp.right.accept(self, env)
            if type(right) != type(True):
                sys.exit("Type error")
            return right

    def visit_fn(self, exp, env):
        # Cria closure: Function(formal, body, env)
        # O nome do parâmetro pode ser 'parameter' ou 'formal' dependendo da AST
        # Ajuste conforme o nome correto
        formal = getattr(exp, 'formal', getattr(exp, 'parameter', None))
        return Function(formal, exp.body, env)

    def visit_app(self, exp, env):
        func = exp.function.accept(self, env)
        arg = exp.argument.accept(self, env)
        if isinstance(func, Function):
            new_env = func.env.copy()
            new_env[func.formal] = arg
            return func.body.accept(self, new_env)
        else:
            sys.exit("Type error")
