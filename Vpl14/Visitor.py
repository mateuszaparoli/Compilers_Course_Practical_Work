import sys
from abc import ABC, abstractmethod
from Expression import *
import Asm as AsmModule


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
    def visit_and(self, exp, arg):
        pass

    @abstractmethod
    def visit_or(self, exp, arg):
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
    def visit_ifThenElse(self, exp, arg):
        pass

    @abstractmethod
    def visit_fn(self, exp, arg):
        pass

    @abstractmethod
    def visit_app(self, exp, arg):
        pass


class RenameVisitor(Visitor):
    def __init__(self):
        self._counter = 0

    def rename(self, base):
        name = f"{base}_{self._counter}"
        self._counter += 1
        return name

    def visit_var(self, exp, name_map):
        map = name_map.get(exp.identifier)
        if map is not None:
            exp.identifier = map

    def visit_bln(self, exp, name_map):
        return None

    def visit_num(self, exp, name_map):
        return None

    def visit_eql(self, exp, name_map):
        exp.left.accept(self, name_map)
        exp.right.accept(self, name_map)

    def visit_and(self, exp, name_map):
        """
        Example:
            >>> y0 = Var('x')
            >>> y1 = Var('x')
            >>> x0 = And(Lth(y0, Num(2)), Leq(Num(2), y1))
            >>> x1 = Var('x')
            >>> e0 = Let('x', Num(2), Add(x0, Num(3)))
            >>> e1 = Let('x', e0, Mul(x1, Num(10)))
            >>> r = RenameVisitor()
            >>> e1.accept(r, {})
            >>> y0.identifier == y1.identifier
            True

            >>> y0 = Var('x')
            >>> y1 = Var('x')
            >>> x0 = And(Lth(y0, Num(2)), Leq(Num(2), y1))
            >>> x1 = Var('x')
            >>> e0 = Let('x', Num(2), Add(x0, Num(3)))
            >>> e1 = Let('x', e0, Mul(x1, Num(10)))
            >>> r = RenameVisitor()
            >>> e1.accept(r, {})
            >>> y0.identifier == x1.identifier
            False
        """
        exp.left.accept(self, name_map)
        exp.right.accept(self, name_map)

    def visit_or(self, exp, name_map):
        """
        Example:
            >>> y0 = Var('x')
            >>> y1 = Var('x')
            >>> x0 = Or(Lth(y0, Num(2)), Leq(Num(2), y1))
            >>> x1 = Var('x')
            >>> e0 = Let('x', Num(2), Add(x0, Num(3)))
            >>> e1 = Let('x', e0, Mul(x1, Num(10)))
            >>> r = RenameVisitor()
            >>> e1.accept(r, {})
            >>> y0.identifier == y1.identifier
            True

            >>> y0 = Var('x')
            >>> y1 = Var('x')
            >>> x0 = Or(Lth(y0, Num(2)), Leq(Num(2), y1))
            >>> x1 = Var('x')
            >>> e0 = Let('x', Num(2), Add(x0, Num(3)))
            >>> e1 = Let('x', e0, Mul(x1, Num(10)))
            >>> r = RenameVisitor()
            >>> e1.accept(r, {})
            >>> y0.identifier == x1.identifier
            False
        """
        exp.left.accept(self, name_map)
        exp.right.accept(self, name_map)

    def visit_add(self, exp, name_map):
        exp.left.accept(self, name_map)
        exp.right.accept(self, name_map)

    def visit_sub(self, exp, name_map):
        exp.left.accept(self, name_map)
        exp.right.accept(self, name_map)

    def visit_mul(self, exp, name_map):
        exp.left.accept(self, name_map)
        exp.right.accept(self, name_map)

    def visit_div(self, exp, name_map):
        exp.left.accept(self, name_map)
        exp.right.accept(self, name_map)

    def visit_leq(self, exp, name_map):
        exp.left.accept(self, name_map)
        exp.right.accept(self, name_map)

    def visit_lth(self, exp, name_map):
        exp.left.accept(self, name_map)
        exp.right.accept(self, name_map)

    def visit_neg(self, exp, name_map):
        exp.exp.accept(self, name_map)

    def visit_not(self, exp, name_map):
        exp.exp.accept(self, name_map)

    def visit_let(self, exp, name_map):
        exp.exp_def.accept(self, name_map)
        originalId = exp.identifier
        newId = self.rename(originalId)
        exp.identifier = newId
        extended_map = dict(name_map)
        extended_map[originalId] = newId
        exp.exp_body.accept(self, extended_map)

    def visit_ifThenElse(self, exp, name_map):
        exp.cond.accept(self, name_map)
        exp.e0.accept(self, name_map)
        exp.e1.accept(self, name_map)

    def visit_fn(self, exp, name_map):
        originalId = exp.formal
        newId = self.rename(originalId)
        exp.formal = newId
        extended_map = dict(name_map)
        extended_map[originalId] = newId
        exp.body.accept(self, extended_map)

    def visit_app(self, exp, name_map):
        exp.function.accept(self, name_map)
        exp.actual.accept(self, name_map)


class GenVisitor(Visitor):
    """
    The GenVisitor class compiles arithmetic expressions into a low-level
    language.
    """

    def __init__(self):
        self.next_var_counter = 0

    def next_var_name(self):
        self.next_var_counter += 1
        return f"tmp{self.next_var_counter}"

    def visit_var(self, exp, prog):
        """
        Usage:
            >>> e = Var('x')
            >>> p = AsmModule.Program({"x":1}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            1
        """
        return exp.identifier

    def visit_bln(self, exp, env):
        """
        Usage:
            >>> e = Bln(True)
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            1

            >>> e = Bln(False)
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            0
        """
        dest = self.next_var_name()
        value = 1 if exp.bln else 0
        env.add_inst(AsmModule.Addi(dest, "x0", value))
        return dest

    def visit_num(self, exp, prog):
        """
        Usage:
            >>> e = Num(13)
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            13
        """
        dest = self.next_var_name()
        prog.add_inst(AsmModule.Addi(dest, "x0", exp.num))
        return dest

    def visit_eql(self, exp, prog):
        """
        >>> e = Eql(Num(13), Num(13))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Eql(Num(13), Num(10))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Eql(Num(-1), Num(1))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0
        """
        left_var = exp.left.accept(self, prog)
        right_var = exp.right.accept(self, prog)
        diff = self.next_var_name()
        prog.add_inst(AsmModule.Sub(diff, left_var, right_var))
        lt_one = self.next_var_name()
        prog.add_inst(AsmModule.Slti(lt_one, diff, 1))
        lt_zero = self.next_var_name()
        prog.add_inst(AsmModule.Slti(lt_zero, diff, 0))
        result = self.next_var_name()
        prog.add_inst(AsmModule.Xor(result, lt_one, lt_zero))
        return result
    
    def visit_and(self, exp, prog):
        """
        >>> e = And(Bln(True), Bln(True))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = And(Bln(False), Bln(True))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = And(Bln(True), Bln(False))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = And(Bln(False), Bln(False))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = And(Bln(False), Div(Num(3), Num(0)))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0
        """
        left_var = exp.left.accept(self, prog)
        beq = AsmModule.Beq(left_var, "x0")
        prog.add_inst(beq)
        right_var = exp.right.accept(self, prog)
        dest = self.next_var_name()

        prog.add_inst(AsmModule.Add(dest, right_var, "x0"))

        jmp = AsmModule.Jal("x0")
        prog.add_inst(jmp)

        beq.set_target(prog.get_number_of_instructions())

        prog.add_inst(AsmModule.Addi(dest, "x0", 0))

        jmp.set_target(prog.get_number_of_instructions())
        return dest

    def visit_or(self, exp, prog):
        """
        >>> e = Or(Bln(True), Bln(True))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Or(Bln(False), Bln(True))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Or(Bln(True), Bln(False))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Or(Bln(False), Bln(False))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Or(Bln(True), Div(Num(3), Num(0)))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1
        """
        left_var = exp.left.accept(self, prog)
        beq = AsmModule.Beq(left_var, "x0")
        prog.add_inst(beq)

        dest = self.next_var_name()
        prog.add_inst(AsmModule.Addi(dest, "x0", 1))

        jmp = AsmModule.Jal("x0")
        prog.add_inst(jmp)

        beq.set_target(prog.get_number_of_instructions())

        right_var = exp.right.accept(self, prog)
        prog.add_inst(AsmModule.Add(dest, right_var, "x0"))

        jmp.set_target(prog.get_number_of_instructions())
        return dest


    def visit_add(self, exp, prog):
        """
        >>> e = Add(Num(13), Num(-13))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Add(Num(13), Num(10))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        23
        """
        left_var = exp.left.accept(self, prog)
        right_var = exp.right.accept(self, prog)
        dest = self.next_var_name()
        prog.add_inst(AsmModule.Add(dest, left_var, right_var))
        return dest

    def visit_sub(self, exp, prog):
        """
        >>> e = Sub(Num(13), Num(-13))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        26

        >>> e = Sub(Num(13), Num(10))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        3
        """
        left_var = exp.left.accept(self, prog)
        right_var = exp.right.accept(self, prog)
        dest = self.next_var_name()
        prog.add_inst(AsmModule.Sub(dest, left_var, right_var))
        return dest

    def visit_mul(self, exp, prog):
        """
        >>> e = Mul(Num(13), Num(2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        26

        >>> e = Mul(Num(13), Num(10))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        130
        """
        left_var = exp.left.accept(self, prog)
        right_var = exp.right.accept(self, prog)
        dest = self.next_var_name()
        prog.add_inst(AsmModule.Mul(dest, left_var, right_var))
        return dest

    def visit_div(self, exp, prog):
        """
        >>> e = Div(Num(13), Num(2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        6

        >>> e = Div(Num(13), Num(10))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1
        """
        left_var = exp.left.accept(self, prog)
        right_var = exp.right.accept(self, prog)
        dest = self.next_var_name()
        prog.add_inst(AsmModule.Div(dest, left_var, right_var))
        return dest

    def visit_leq(self, exp, prog):
        """
        >>> e = Leq(Num(3), Num(2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Leq(Num(3), Num(3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Leq(Num(2), Num(3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Leq(Num(-3), Num(-2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Leq(Num(-3), Num(-3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Leq(Num(-2), Num(-3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0
        """
        left_var = exp.left.accept(self, prog)
        right_var = exp.right.accept(self, prog)
        lower_than = self.next_var_name()
        prog.add_inst(AsmModule.Slt(lower_than, right_var, left_var))
        dest = self.next_var_name()
        prog.add_inst(AsmModule.Xori(dest, lower_than, 1))
        return dest

    def visit_lth(self, exp, prog):
        """
        >>> e = Lth(Num(3), Num(2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Lth(Num(3), Num(3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Lth(Num(2), Num(3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1
        """
        left_var = exp.left.accept(self, prog)
        right_var = exp.right.accept(self, prog)
        dest = self.next_var_name()
        prog.add_inst(AsmModule.Slt(dest, left_var, right_var))
        return dest

    def visit_neg(self, exp, prog):
        """
        >>> e = Neg(Num(3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        -3

        >>> e = Neg(Num(0))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Neg(Num(-3))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        3
        """
        operand = exp.exp.accept(self, prog)
        dest = self.next_var_name()
        prog.add_inst(AsmModule.Sub(dest, "x0", operand))
        return dest

    def visit_not(self, exp, prog):
        """
        >>> e = Not(Bln(True))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Not(Bln(False))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Not(Num(0))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        1

        >>> e = Not(Num(-2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0

        >>> e = Not(Num(2))
        >>> p = AsmModule.Program({}, [])
        >>> g = GenVisitor()
        >>> v = e.accept(g, p)
        >>> p.eval()
        >>> p.get_val(v)
        0
        """
        operand = exp.exp.accept(self, prog)
        lt_one = self.next_var_name()
        prog.add_inst(AsmModule.Slti(lt_one, operand, 1))
        lt_zero = self.next_var_name()
        prog.add_inst(AsmModule.Slti(lt_zero, operand, 0))
        dest = self.next_var_name()
        prog.add_inst(AsmModule.Xor(dest, lt_one, lt_zero))
        return dest

    def visit_let(self, exp, prog):
        """
        Usage:
            >>> e = Let('v', Not(Bln(False)), Var('v'))
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            1

            >>> e = Let('v', Num(2), Add(Var('v'), Num(3)))
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            5

            >>> e0 = Let('x', Num(2), Add(Var('x'), Num(3)))
            >>> e1 = Let('y', e0, Mul(Var('y'), Num(10)))
            >>> p = AsmModule.Program({}, [])
            >>> g = GenVisitor()
            >>> v = e1.accept(g, p)
            >>> p.eval()
            >>> p.get_val(v)
            50
        """
        value_var = exp.exp_def.accept(self, prog)
        
        # Check if the definition is a lambda - if so, we need special handling
        from Expression import Fn as FnExpr
        if isinstance(exp.exp_def, FnExpr):
            # For lambdas, the value is a closure tuple stored in value_var
            # Just copy the closure reference
            prog.set_val(exp.identifier, prog.get_val(value_var))
        else:
            # For non-lambda expressions, use Add to copy the value at runtime
            prog.add_inst(AsmModule.Add(exp.identifier, value_var, "x0"))
        
        return exp.exp_body.accept(self, prog)

    def visit_ifThenElse(self, exp, prog):
        """
        Handles if-then-else expressions
        """
        cond_var = exp.cond.accept(self, prog)
        beq = AsmModule.Beq(cond_var, "x0")
        prog.add_inst(beq)
        
        e0_var = exp.e0.accept(self, prog)
        dest = self.next_var_name()
        prog.add_inst(AsmModule.Add(dest, e0_var, "x0"))
        
        jmp = AsmModule.Jal("x0")
        prog.add_inst(jmp)
        
        beq.set_target(prog.get_number_of_instructions())
        
        e1_var = exp.e1.accept(self, prog)
        prog.add_inst(AsmModule.Add(dest, e1_var, "x0"))
        
        jmp.set_target(prog.get_number_of_instructions())
        return dest

    def visit_fn(self, exp, prog):
        closure_id = self.next_var_name()
        current_env = dict(prog._Program__env)
        prog.set_val(closure_id, ("closure", exp.formal, exp.body, current_env))
        return closure_id

    def visit_app(self, exp, prog):
        """
        Handles function application by inlining the lambda body
        with the argument substituted for the formal parameter.
        """
        # Import here to avoid circular imports
        from Expression import Fn as FnExpr, App, Var
        
        if isinstance(exp.function, FnExpr):
            arg_var = exp.actual.accept(self, prog)
            
            formal = exp.function.formal
            body = exp.function.body
            import copy
            body_copy = copy.deepcopy(body)
            
            # Rename all occurrences of the formal parameter to the argument variable
            rename_map = {formal: arg_var}
            body_copy.accept(RenameVisitor(), rename_map)
            
            # Generate code for the substituted body
            return body_copy.accept(self, prog)
        else:
            # Function is a variable holding a closure
            # This is more complex - evaluate the function first
            fn_var = exp.function.accept(self, prog)
            arg_var = exp.actual.accept(self, prog)
            
            # Get the closure tuple from the environment
            # The function should have stored a closure when visit_fn was called
            if fn_var not in prog._Program__env:
                # If the function variable is not in the environment, it might be because
                # we're in a nested context. For now, just return fn_var as-is
                result = self.next_var_name()
                prog.add_inst(AsmModule.Add(result, fn_var, "x0"))
                return result
            
            closure_tuple = prog.get_val(fn_var)
            
            # Extract components from the closure
            if isinstance(closure_tuple, tuple) and closure_tuple[0] == "closure":
                _, formal_param, body_expr, captured_env = closure_tuple
                
                # Create a copy of the body
                import copy
                body_copy = copy.deepcopy(body_expr)
                
                # Create a rename map to substitute the formal parameter
                rename_map = {formal_param: arg_var}
                body_copy.accept(RenameVisitor(), rename_map)
                
                # Generate code for the body WITHOUT changing the environment
                # (the captured environment is already in the closure, so references
                # to outer variables should still work)
                result = body_copy.accept(self, prog)
                
                return result
            else:
                # Not a valid closure
                result = self.next_var_name()
                prog.add_inst(AsmModule.Add(result, fn_var, "x0"))
                return result

