import numpy

class Variable(object):
    def __init__(self, name, inverted=False):
        self.name = name
        self.inverted = inverted

    def __neg__(self):
        v = Variable(self.name)
        v.inverted = not self.inverted
        return v

    def __and__(self, other):
        c = Cnf.create_from(self)
        return c & other

    def __or__(self, other):
        c = Cnf.create_from(self)
        return c | other

    def __xor__(self, other):
        c = Cnf.create_from(self)
        return c ^ other

    def __rshift__(self, other): # implies
        c = Cnf.create_from(self)
        return -c | other

    def __str__(self):
        return ("-" if self.inverted else "") + self.name

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

class Cnf(object):
    def __init__(self):
        self.dis = []

    @classmethod
    def create_from(cls, x):
        if isinstance(x, Variable):
            cnf = Cnf()
            cnf.dis = [frozenset([x])]
            return cnf
        elif isinstance(x, cls):
            return x
        else:
            raise Exception("Could not create a Cnf object from %s" % str(type(x)))

    def __and__(self, other):
        other = Cnf.create_from(other)
        result = Cnf()
        result.dis = self.dis + other.dis
        return result

    def __or__(self, other):
        other = Cnf.create_from(other)

        if len(self.dis) > 0 and len(other.dis) > 0:
            new_dis = []
            for d1, d2 in [(d1,d2) for d1 in self.dis for d2 in other.dis]:
                d3 = d1 | d2
                new_dis.append(d3)
        elif len(self.dis) == 0:
            new_dis = other.dis
        else:
            new_dis = self.dis

        c = Cnf()
        c.dis = new_dis
        return c

    def __xor__(self, other):
        return (self | other) & (-self | -other)

    def __neg__(self):
        cnfs = []

        for d in self.dis:
            c = Cnf()
            for v in d:
                c.dis.append(frozenset([-v]))
            cnfs.append(c)

        ret = cnfs.pop()
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
