from satispy import Cnf, Variable

class DimacsCnf(object):
    def __init__(self):
        self.varname_dict = {}
        self.varobj_dict = {}

    def varname(self, vo):
        return self.varname_dict[vo]

    def varobj(self, v):
        return self.varobj_dict[v]

    def tostring(self, cnf):
        """Convert Cnf object ot Dimacs cnf string
        
        cnf: Cnf object
        
        In the converted Cnf there will be only numbers for
        variable names. The conversion guarantees that the
        variables will be numbered alphabetically.
        """
        self.varname_dict = {}
        self.varobj_dict = {}

        varis = set()
        for d in cnf.dis:
            for v in d:
                varis.add(v.name)

        ret = "p cnf %d %d" % (len(varis), len(cnf.dis))

        varis = dict(zip(sorted(list(varis)),map(str,range(1,len(varis)+1))))

        for v in varis:
            vo = Variable(v)
            self.varname_dict[vo] = varis[v]
            self.varobj_dict[varis[v]] = vo

        for d in cnf.dis:
            ret += "\n"
            vnamelist = []
            for v in d:
                vnamelist.append(("-" if v.inverted else "") + varis[v.name])
            ret += " ".join(vnamelist) + " 0"

        return ret

    def fromstring(self, s):
        self.varname_dict = {}
        self.varobj_dict = {}

        lines = s.split("\n")
        # Throw away comments and empty lines
        new_lines = []
        for l in lines:
            l = l.strip()
            if l[0] != 'c' and l != "":
                new_lines.append(l)

        _,_,varz,clauses = new_lines[0].split(" ")
        varz, clauses = int(varz), int(clauses)

        c = Cnf()

        lines = new_lines[1:]
        for line in lines:
            c.dis.append(frozenset(map(lambda vn: Variable("v"+vn.strip(" \t\r\n-"), vn[0] == '-'), line.split(" ")[:-1])))

        for i in xrange(1,varz+1):
            stri = str(i)
            vo = Variable('v'+stri)
            self.varname_dict[vo] = stri
            self.varobj_dict[stri] = vo

        return c

    def write(self, cnf, fil):
        f = open(fil, 'w')
        f.write(self.tostring(cnf))
        f.close()

    def read(self, fil):
        f = open(fil, 'r')
        cnf = self.fromstring(f.read())
        f.close()
        return cnf
