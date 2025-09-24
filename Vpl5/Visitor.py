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
            raise NameError(f"Variavel inexistente {exp.identifier}")
    
    def visit_bln(self, exp, env):
        return env.get(exp.bln, exp.bln)

    def visit_num(self, exp, env):
        return env.get(exp.num, exp.num)

    def visit_eql(self, exp, env):
        exp_left = exp.left.accept(self, env)
        exp_right = exp.right.accept(self, env)
        return exp_left == exp_right

    def visit_add(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        return int(left + right)
    
    def visit_sub(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        return int(left - right)
    
    def visit_mul(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        return int(left * right)

    def visit_div(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        return int(left / right)

    def visit_leq(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        return left <= right

    def visit_lth(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        return left < right

    def visit_neg(self, exp, env):
        value = exp.exp.accept(self, env)
        return -value

    def visit_not(self, exp, env):
        value = exp.exp.accept(self, env)
        return not value

    def visit_let(self, exp, env):
        value = exp.exp_def.accept(self, env)
        new_env = env.copy()
        new_env[exp.identifier] = value
        return exp.exp_body.accept(self, new_env)
   
class UseDefVisitor(Visitor):
    """
    The UseDefVisitor class reports the use of undefined variables. It takes
    as input an environment of defined variables, and produces, as output,
    the set of all the variables that are used without being defined.

    Examples:
    >>> e0 = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
    >>> e1 = Not(Eql(e0, Num(1764)))
    >>> ev = UseDefVisitor()
    >>> len(e1.accept(ev, set()))
    0

    >>> e0 = Let('v', Add(Num(40), Num(2)), Sub(Var('v'), Num(2)))
    >>> e1 = Lth(e0, Var('x'))
    >>> ev = UseDefVisitor()
    >>> len(e1.accept(ev, set()))
    1

    >>> e = Let('v', Add(Num(40), Var('v')), Sub(Var('v'), Num(2)))
    >>> ev = UseDefVisitor()
    >>> len(e.accept(ev, set()))
    1

    >>> e1 = Let('v', Add(Num(40), Var('v')), Sub(Var('v'), Num(2)))
    >>> e0 = Let('v', Num(3), e1)
    >>> ev = UseDefVisitor()
    >>> len(e0.accept(ev, set()))
    0
    """
    def visit_var(self, exp, defined):
        if exp.identifier in defined:
            return set()
        else:
            return {exp.identifier}

    def visit_bln(self, exp, defined):
        return set()

    def visit_num(self, exp, defined):
        return set()

    def visit_eql(self, exp, defined):
        left = exp.left.accept(self, defined)
        right = exp.right.accept(self, defined)
        return left | right

    def visit_add(self, exp, defined):
        left = exp.left.accept(self, defined)
        right = exp.right.accept(self, defined)
        return left | right

    def visit_sub(self, exp, defined):
        left = exp.left.accept(self, defined)
        right = exp.right.accept(self, defined)
        return left | right

    def visit_mul(self, exp, defined):
        left = exp.left.accept(self, defined)
        right = exp.right.accept(self, defined)
        return left | right

    def visit_div(self, exp, defined):
        left = exp.left.accept(self, defined)
        right = exp.right.accept(self, defined)
        return left | right

    def visit_leq(self, exp, defined):
        left = exp.left.accept(self, defined)
        right = exp.right.accept(self, defined)
        return left | right

    def visit_lth(self, exp, defined):
        left = exp.left.accept(self, defined)
        right = exp.right.accept(self, defined)
        return left | right

    def visit_neg(self, exp, defined):
        return exp.exp.accept(self, defined)

    def visit_not(self, exp, defined):
        return exp.exp.accept(self, defined)

    def visit_let(self, exp, defined):
        used_in_def = exp.exp_def.accept(self, defined)
        new_defined = set(defined)
        new_defined.add(exp.identifier)
        used_in_body = exp.exp_body.accept(self, new_defined)
        return used_in_def | used_in_body

def safe_eval(exp):
    """
    Avalia a expressão apenas se não houver variáveis indefinidas.
    """
    ev = UseDefVisitor()
    undefined_vars = exp.accept(ev, set())
    if undefined_vars:
        print("Error: expression contains undefined variables.")
    else:
        try:
            value = exp.accept(EvalVisitor(), {})
            print(f"Value is {value}")
        except NameError as e:
            print("Error: expression contains undefined variables.")
