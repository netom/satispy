from itertools import product

cnfClass = None

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

# Change this to NaiveCnf if you want.
cnfClass = Cnf
