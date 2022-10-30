from models import Literal, Clause, Cnf
from models import Node, DecisionLevel, Trail
from parse import cnf_parse


class SatSolver:
    """
    Class:
        a SAT solver with CDCL Algorithm
    Attributes:
        cnf: a Cnf class which store the origin Cnf
        trail: a literal sequence with result
    Methods:
        parser: parse the cnf file to a Cnf Class
        solve: solve the SAT Problem by CDCL algorithm
    """
    def __init__(self, cnf: Cnf):
        """
        Method:
            Constructed Function
        """
        self.cnf = cnf
        self.trail = Trail(decision_level_list=[])
        # Use assignments to record the real value of every variable
        self.assignments = dict()
        for clause in cnf.clause_list:
            for literal in clause.literal_list:
                if literal.variable not in self.assignments and (literal.variable-cnf.literal_num) not in self.assignments:
                    # literal or (not literal) are both not in assignments
                    self.assignments[literal.variable] = None


if __name__ == "__main__":
    cnf = cnf_parse("./raw/test.cnf")
    SatSolver(cnf)
