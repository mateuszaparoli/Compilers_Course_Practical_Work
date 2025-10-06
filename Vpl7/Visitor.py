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
        if type(value) not in [type(1), type(True)]:
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
                return exp.then.accept(self, env)
            else:
                return exp.els.accept(self, env)
        
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

    def visit_if(self, exp, defined):
        used_in_cond = exp.cond.accept(self, defined)
        used_in_then = exp.then.accept(self, defined)
        used_in_els = exp.els.accept(self, defined)
        return used_in_cond | used_in_then | used_in_els
    
    def visit_or(self, exp, defined):
        left = exp.left.accept(self, defined)
        right = exp.right.accept(self, defined)
        return left | right
    
    def visit_and(self, exp, defined):
        left = exp.left.accept(self, defined)
        right = exp.right.accept(self, defined)
        return left | right

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
           
class CtrGenVisitor(Visitor):
    """
    This visitor creates constraints for a type-inference engine. Basically,
    it traverses the abstract-syntax tree of expressions, producing pairs like
    (type0, type1) on the way. A pair like (type0, type1) indicates that these
    two type variables are the same.

    Examples:
        >>> e = Let('v', Num(40), Let('w', Num(2), Add(Var('v'), Var('w'))))
        >>> ev = CtrGenVisitor()
        >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
        ["('TV_1', 'TV_2')", "('TV_2', 'TV_3')", "('v', <class 'int'>)", "('w', <class 'int'>)", "(<class 'int'>, 'TV_3')", "(<class 'int'>, 'v')", "(<class 'int'>, 'w')"]
    """

    def __init__(self):
        self.fresh_type_counter = 0

    def fresh_type_var(self):
        """
        Create a new type var using the current value of the fresh_type_counter.
        Two successive calls to this method will return different type names.
        Notice that the name of a type variable is always TV_x, where x is
        some integer number. That means that probably we would run into
        errors if someone declares a variable called, say, TV_1 or TV_2, as in
        "let TV_1 <- 1 in TV_1 end". But you can assume that such would never
        happen in the test cases. In practice, we should define a new class
        to represent type variables. But let's keep the implementation as
        simple as possible.

        Example:
            >>> ev = CtrGenVisitor()
            >>> [ev.fresh_type_var(), ev.fresh_type_var()]
            ['TV_1', 'TV_2']
        """
        self.fresh_type_counter += 1
        return f"TV_{self.fresh_type_counter}"

    """
    The CtrGenVisitor class creates constraints that, once solved, will give
    us the type of the different variables. Every accept method takes in
    two arguments (in addition to self):
    
    exp: is the expression that is being analyzed.
    type_var: that is a name that works as a placeholder for the type of the
    expression. Whenever we visit a new expression, we create a type variable
    to represent its type (you can do that with the method fresh_type_var).
    The only exception is the type of Var expressions. In this case, the type
    of a Var expression is the identifier of that expression.
    """

    def visit_var(self, exp, type_var):
        """
        Example:
            >>> e = Var('v')
            >>> ev = CtrGenVisitor()
            >>> e.accept(ev, ev.fresh_type_var())
            {('v', 'TV_1')}
        """
        return {(exp.identifier, type_var)}

    def visit_bln(self, exp, type_var):
        """
        Example:
            >>> e = Bln(True)
            >>> ev = CtrGenVisitor()
            >>> e.accept(ev, ev.fresh_type_var())
            {(<class 'bool'>, 'TV_1')}
        """
        return {(type(True), type_var)}

    def visit_num(self, exp, type_var):
        """
        Example:
            >>> e = Num(1)
            >>> ev = CtrGenVisitor()
            >>> e.accept(ev, ev.fresh_type_var())
            {(<class 'int'>, 'TV_1')}
        """
        return {(type(1), type_var)}

    def visit_eql(self, exp, type_var):
        """
        Example:
            >>> e = Eql(Num(1), Bln(True))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'bool'>, 'TV_2')", "(<class 'int'>, 'TV_2')"]

        Notice that if we have repeated constraints, they only appear once in
        the set of constraints (after all, it's a set!). As an example, we
        would have two occurrences of the pair (TV_2, int) in the following
        example:
            >>> e = Eql(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'int'>, 'TV_2')"]
        """
        # TODO: Implement this method!
        # Acho que ta errado isso aqui, entender melhor e continuar daqui
        left = exp.left.accept(self, type_var)
        right = exp.right.accept(self, type_var)
        return {(type(left), type(right))}

    def visit_and(self, exp, type_var):
        """
        Example:
            >>> e = And(Bln(False), Bln(True))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'bool'>, <class 'bool'>)"]

        In the above example, notice that we ended up getting a trivial
        constraint, e.g.: (<class 'bool'>, <class 'bool'>). That's alright:
        don't worry about these trivial constraints at this point. We can
        remove them from the set of constraints later on, when we try to
        solve them.
        """
        # TODO: Implement this method!
        raise NotImplementedError

    def visit_or(self, exp, type_var):
        """
        Example:
            >>> e = Or(Bln(False), Bln(True))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'bool'>, <class 'bool'>)"]
        """
        # TODO: Implement this method!
        raise NotImplementedError

    def visit_add(self, exp, type_var):
        """
        Example:
            >>> e = Add(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'int'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        # TODO: Implement this method!
        raise NotImplementedError

    def visit_sub(self, exp, type_var):
        """
        Example:
            >>> e = Sub(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'int'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        # TODO: Implement this method!
        raise NotImplementedError

    def visit_mul(self, exp, type_var):
        """
        Example:
            >>> e = Mul(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'int'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        # TODO: Implement this method!
        raise NotImplementedError

    def visit_div(self, exp, type_var):
        """
        Example:
            >>> e = Div(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'int'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        # TODO: Implement this method!
        raise NotImplementedError

    def visit_leq(self, exp, type_var):
        """
        Example:
            >>> e = Leq(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        # TODO: Implement this method!
        raise NotImplementedError

    def visit_lth(self, exp, type_var):
        """
        Example:
            >>> e = Lth(Num(1), Num(2))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        # TODO: Implement this method!
        raise NotImplementedError

    def visit_neg(self, exp, type_var):
        """
        Example:
            >>> e = Neg(Num(1))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'int'>, 'TV_1')", "(<class 'int'>, <class 'int'>)"]
        """
        # TODO: Implement this method!
        raise NotImplementedError

    def visit_not(self, exp, type_var):
        """
        Example:
            >>> e = Not(Bln(True))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["(<class 'bool'>, 'TV_1')", "(<class 'bool'>, <class 'bool'>)"]
        """
        # TODO: Implement this method!
        raise NotImplementedError

    def visit_let(self, exp, type_var):
        """
        Example:
            >>> e = Let('v', Num(42), Var('v'))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["('TV_1', 'TV_2')", "('v', 'TV_2')", "(<class 'int'>, 'v')"]
        """
        # TODO: Implement this method!
        raise NotImplementedError

    def visit_ifThenElse(self, exp, type_var):
        """
        Example:
            >>> e = IfThenElse(Bln(True), Num(42), Num(30))
            >>> ev = CtrGenVisitor()
            >>> sorted([str(ct) for ct in e.accept(ev, ev.fresh_type_var())])
            ["('TV_1', 'TV_2')", "(<class 'bool'>, <class 'bool'>)", "(<class 'int'>, 'TV_2')"]
        """
        # TODO: Implement this method!
        raise NotImplementedError
