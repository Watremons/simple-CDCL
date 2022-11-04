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
        self.now_decision_level = 0;
        for clause in cnf.clause_list:
            for literal in clause.literal_list:
                if literal.variable not in self.assignments and (literal.variable-cnf.variable_num) not in self.assignments:
                    # literal or (not literal) are both not in assignments
                    self.assignments[literal.variable] = None

    def unit_propagate(self, cnf_copy):
        pass

    def conflict_analyze(self, cnf_copy) -> Clause:
        pass

    def backtrack(self):
        pass

    def make_new_decision_level(self):
        pass

    def get_new_unknown_literal(self, cnf_copy):
        pass

    def unknown_variable_exists(self):
        pass

    def has_flase_clause(self):
        pass

    def solve(self):
        cnf_copy = self.cnf
        while True:
            # do BCP process
            cnf_copy = self.unit_propagate(cnf_copy)
            # do "conflict analysis" process
            if self.has_flase_clause(cnf_copy):
                if self.now_decision_level == 0:
                    return False
                new_clause = self.conflict_analyze(cnf_copy)
                self.cnf.append_clause(new_clause)
                # do BACKTRACK process
                self.backtrack()
            else:
                if not self.unknown_variable_exists(cnf_copy):
                    return True
                # do DECIDE process
                self.make_new_decision_level()
                l = self.get_new_unknown_literal(cnf_copy)
                cnf_copy = cnf_copy.append(l)

if __name__ == "__main__":
    cnf = cnf_parse("./raw/test.cnf")
    SatSolver(cnf)
