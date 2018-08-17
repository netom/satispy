from __future__ import absolute_import
from itertools import product
from six.moves import map
from functools import total_ordering

cnfClass = None

@total_ordering
class Variable(object):
    def __init__(self, name, inverted=False):
        self.name = name
        self.inverted = inverted

    def __neg__(self):
        v = Variable(self.name)
        v.inverted = not self.inverted
        return v

    def __and__(self, other):
        c = cnfClass.create_from(self)
        return c & other

    def __or__(self, other):
        c = cnfClass.create_from(self)
        return c | other

    def __xor__(self, other):
        c = cnfClass.create_from(self)
        return c ^ other

    def __rshift__(self, other): # implies
        c = cnfClass.create_from(self)
        return -c | other

    def __str__(self):
        return ("-" if self.inverted else "") + str(self.name)

    def __eq__(self, other):
        return self.name == other.name and self.inverted == other.inverted

    def __hash__(self):
        return hash(self.name) ^ hash(self.inverted)

    def __cmp__(self, other):
        if self == other:
            return 0
        if (self.name, self.inverted) < (other.name, other.inverted):
            return -1
        else:
            return 1

    def __lt__(self, other):
        return self.__cmp__(other) == -1

class NaiveCnf(object):
    def __init__(self):
        self.dis = frozenset()

    @classmethod
    def create_from(cls, x):
        if isinstance(x, Variable):
            cnf = NaiveCnf()
            cnf.dis = frozenset([frozenset([x])])
            return cnf
        elif isinstance(x, cls):
            return x
        else:
            raise Exception("Could not create a Cnf object from %s" % str(type(x)))

    def __and__(self, other):
        other = NaiveCnf.create_from(other)
        result = NaiveCnf()
        result.dis = self.dis | other.dis
        return result

    def __or__(self, other):
        other = NaiveCnf.create_from(other)

        if self.dis and other.dis:
            new_dis = frozenset(
                d1 | d2
                for d1, d2 in product(self.dis, other.dis)
            )
        elif other.dis:
            new_dis = other.dis
        else:
            new_dis = self.dis

        c = NaiveCnf()
        c.dis = new_dis
        return c

    def __xor__(self, other):
        return (self | other) & (-self | -other)

    def __neg__(self):
        cnfs = []

        for d in self.dis:
            c = NaiveCnf()
            c.dis = frozenset(
                frozenset([-v])
                for v in d
            )
            cnfs.append(c)

        ret = NaiveCnf()
        for cnf in cnfs:
            ret |= cnf

        return ret

    def __rshift__(self, other): # implies
        return -self | other

    def __str__(self):
        ret = []
        for d in self.dis:
            ret.append(" | ".join(map(str,d)))
        return "(" + ") & (".join(ret) + ")"

    def __eq__(self, other):
        return self.dis == other.dis

    def __hash__(self):
        return hash(self.dis)

def reduceCnf(cnf):
    """
    I just found a remarkably large bug in my SAT solver and found an
    interesting solution.
    Remove all b | -b
    (-b | b) & (b | -a) & (-b | a) & (a | -a)
    becomes
    (b | -a) & (-b | a)

    Remove all (-e) & (-e)
    (-e | a) & (-e | a) & (-e | a) & (-e | a)
    becomes
    (-e | a)
    (-b | b | c) becomes nothing, not (c)
    """
    output = Cnf()
    for x in cnf.dis:
        dont_add = False
        for y in x:
            for z in x:
                if z == -y:
                    dont_add = True
                    break
            if dont_add: break
        if dont_add: continue
        # TODO: Is this necessary anymore? Probably not. Do statistical analysis.
        if x not in output.dis:
            output.dis |= frozenset([x])
    return output
#end def reduceCnf(cnf)

class Cnf(object):
    def __init__(self):
        self.dis = frozenset()

    @classmethod
    def create_from(cls, x):
        if isinstance(x, Variable):
            cnf = Cnf()
            cnf.dis = frozenset([frozenset([x])])
            return cnf
        elif isinstance(x, cls):
            return x
        else:
            raise Exception("Could not create a Cnf object from %s" % str(type(x)))

    def __and__(self, other):
        other = Cnf.create_from(other)
        result = Cnf()
        result.dis = self.dis | other.dis
        return result

    def __or__(self, other):
        other = Cnf.create_from(other)

        if self.dis and other.dis:
            new_dis = frozenset(
                d1 | d2
                for d1, d2 in product(self.dis, other.dis)
            )
        elif other.dis:
            new_dis = other.dis
        else:
            new_dis = self.dis

        c = Cnf()
        c.dis = new_dis
        return reduceCnf(c)

    def __xor__(self, other):
        return reduceCnf((self | other) & (-self | -other))

    def __neg__(self):
        cnfs = []

        for d in self.dis:
            c = Cnf()
            c.dis = frozenset(
                frozenset([-v])
                for v in d
            )
            x = reduceCnf(c)
            if x not in cnfs:
                cnfs.append(x)

        ret = Cnf()
        for cnf in cnfs:
            ret |= cnf

        return ret

    def __rshift__(self, other): # implies
        return -self | other

    def __str__(self):
        ret = []
        for d in self.dis:
            ret.append(" | ".join(map(str,d)))
        return "(" + ") & (".join(ret) + ")"

    def __eq__(self, other):
        return self.dis == other.dis

    def __hash__(self):
        return hash(self.dis)


class CnfFromString(Cnf):
    def __init__(self):
        pass

    @staticmethod
    def create(string):
        output_queue, symbols = CnfFromString.string_to_rpn(string)
        return CnfFromString.execute_rpn(output_queue), symbols

    @staticmethod
    def string_to_rpn(string):
        # Convert string to RPN using the railroad-shunt algorithm

        symbols = {} # list of 'Variable' objects; keys are strings used as names in input
        current_token = ''

        output_queue = []
        stack = []

        for i in range(0, len(string)):
            ch = string[i]
            operator_char = (ch in ["-", "&", "|", "^", ">", " ", "(", ")"])

            # reached end of variable-name token
            if current_token and operator_char:
                if current_token not in symbols.keys():
                    symbols[current_token] = Variable(current_token)

                output_queue.append(symbols[current_token])
                current_token = ''

            elif current_token and i == len(string)-1:

                if not operator_char:
                    current_token += ch

                if current_token not in symbols.keys():
                    symbols[current_token] = Variable(current_token)

                output_queue.append(symbols[current_token])
                current_token = ''


            if ch in ["-", "&", "|", "^", '>']:

                # don't let unary '-' operator pop a binary operator from the stack
                # give parens a high precedence
                if stack and ch != "-" and stack[-1] != '(':
                    output_queue.append(stack.pop())

                    # if popped a minus, pop again?
                    if output_queue[-1] == "-" and stack and stack[-1] != '(':
                        output_queue.append(stack.pop())

                if ch == ">" and string[i+1] != ">":
                    print("Error: single '>' is not allowed")
                    return
                if ch == ">" and string[i+1] == ">":
                    stack.append(ch)
                    i += 1
                else:
                    stack.append(ch)

            if ch == "(":
                stack.append("(")

            if ch == ")":
                while True:
                    next_operator = stack.pop()
                    if next_operator == "(":
                        break
                    output_queue.append(next_operator)

            if  ch not in ["-", "&", "|", "^", '>', "(", ")", " "]:
                current_token += ch

        while stack:
            output_queue.append(stack.pop())

        return output_queue, symbols

    @staticmethod
    def execute_rpn(output_queue):
        result_stack = []
        i = 0
        while i < len(output_queue):

            # n.b. operators were recorded as strings, whislt variables are Variable objects
            if not isinstance(output_queue[i], str):
                # not an operator
                result_stack.append(output_queue[i])

            elif output_queue[i] == "-":
                # negation
                result_stack[-1] = result_stack[-1].__neg__()

            else:
                # other operator
                operator = output_queue[i]
                rarg = result_stack.pop()
                larg = result_stack.pop()

                result_stack.append(CnfFromString.apply_operator(larg, rarg, operator))

            i += 1

        return result_stack[0]

    @staticmethod
    def apply_operator(larg, rarg, operator):
        if operator == "&":
            return larg.__and__(rarg)
        elif operator == "|":
            return larg.__or__(rarg)
        elif operator == "^":
            return larg.__xor__(rarg)
        elif operator == ">>":
            return larg.rshift(rarg)




# Change this to NaiveCnf if you want.
cnfClass = Cnf
