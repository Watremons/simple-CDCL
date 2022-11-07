# Stardard lib
from copy import deepcopy

# Customized lib
from models import Literal, Clause, Cnf
from models import Node, Trail
from parse import cnf_parse
from utils import resolute_clause, to_clause, to_variable


class SatSolver:
    """
    Class:
        a SAT solver with CDCL Algorithm
    Attributes:
        cnf: a Cnf class which store the origin Cnf
        trail: a literal sequence with result
        variable_to_node: a dict stored the mapping from variable to node
        assignments: record the variable to assigned node
    Methods:
        solve: solve the SAT Problem by CDCL algorithm
        is_study_clause: judge whether a conflict_clause is a study clause and return a literal in conflict_level
    """
    def __init__(self, cnf: Cnf):
        """
        Method:
            Constructed Function
        """
        self.cnf = cnf
        self.trail = Trail(node_list=[])
        self.variable_to_node = dict()
        self.assignments = dict()
        self.now_decision_level = 0
        for clause in cnf.clause_list:
            for literal in clause.literal_list:
                if literal.variable not in self.assignments and (literal.variable-cnf.variable_num) not in self.assignments:
                    # literal or (not literal) are both not in assignments
                    self.assignments[literal.variable] = None

    def is_study_clause(self, conflict_clause: Clause, conflict_level: int) -> tuple[bool, Node]:
        """
        Method:
            judge whether a conflict_clause is a study clause and return a literal in conflict_level
            a study clause has only one variable at conflict level
        Params:
            conflict_clause: the conflict clause to be judged
            conflict_level: the decision level which conflict occurred
        Return:
            flag: whether a conflict_clause is a study clause
            Node: the first node at confilct level whose variable is included in conflict clause
        """
        count = 0
        max_index = -1
        max_index_node = None
        for conflict_literal in conflict_clause.literal_list:
            conflict_variable = conflict_literal.variable
            variable_node = self.variable_to_node[conflict_variable]
            if variable_node.level == conflict_level:
                count += 1
                # TODO: set the index
                if max_index < variable_node.index:
                    max_index = variable_node.index
                    max_index_node = variable_node

        return count == 1, max_index_node

    def unit_propagate(self):
        # Do with self.cnf
        pass

    def conflict_analyze(self) -> tuple[Clause, int]:
        """
        Method:
            analyze the trail when cnf have a false clause
            1.Get conflict node at the end of trail and trans to conflict clause
            2.Check the conflict clause has only one literal at conflict level, if not, use the clause at conflict level to resolute excess literals
            3.Record the backtrack decision level
            4.Return
        Return:
            study_clause: the clause which study from the conflict
            backtrack_decision_level: the decision level which need to backtrack
        """
        # Do with self.cnf
        # 1.Get conflict node at the end of trail
        last_decision_level = self.now_decision_level
        conflict_node = self.trail.node_list[-1]
        assert conflict_node.reason is not None, "Error: Can't get the conflict clause at the end of trail"

        reason_literal_list = []
        for reason_literal in conflict_node.reason:
            variable, sign = to_variable(reason_literal, self.cnf.variable_num)
            reason_literal_list.append(Literal(variable=variable, sign=sign, literal=reason_literal))
        conflict_clause = Clause(literal_list=reason_literal_list)

        # 2.Check the conflict clause has only one literal at conflict level
        # if not, use the clause at conflict level to resolute excess literals
        while True:
            flag, latest_conflict_level_node = self.is_study_clause(conflict_clause, last_decision_level)
            if flag:
                break
            to_resolute_clause = to_clause(latest_conflict_level_node, self.cnf.variable_num)

            conflict_clause = resolute_clause(
                conflict_clause=conflict_clause,
                to_resolute_clause=to_resolute_clause,
                variable=latest_conflict_level_node.variable,
                variable_num=self.cnf.variable_num
            )

        study_clause = conflict_clause
        # 3.Record the backtrack decision level
        if len(conflict_clause.literal_list) == 1:
            # return to level 0 if study clause has only one literal
            backtrack_decision_level = 0
        else:
            # return to target level if study clause has more than one literal
            study_clause_decision_level_set = set()
            for reason_literal in conflict_clause.literal_list:
                study_clause_decision_level_set.add(self.variable_to_node[reason_literal.variable].level)
            backtrack_decision_level = list(study_clause_decision_level_set).sort(reverse=False)[-2]
        # 4.Return
        return study_clause, backtrack_decision_level

    def backtrack(self, back_level: int) -> None:
        """
        Method:
            Use the cnf which adds the study clause and backtrack decision level to do backtrack
            1.Set now decision level to the backtrack level
            2.Remove all nodes whose level is greater than back_level from trail
        Params:
            back_level: the decision level that the solver need to backtrack to
        """
        while True:
            if len(self.trail.node_list) == 0:
                # break if no node remain
                break
            last_node = self.trail.node_list.pop()
            if last_node.level <= back_level:
                # break
                break
            else:
                if last_node.variable is not None:
                    self.variable_to_node.pop(last_node.variable)
                del last_node

    def make_new_decision_level(self):
        pass

    def get_new_unknown_literal(self):
        # Do with self.cnf
        pass

    def unknown_variable_exists(self):
        pass

    def detect_false_clause(self):
        # TODO: Add the conflict clause to trail if detecting a false clause
        pass

    def print_result(self, raw_cnf: Cnf):
        """
        Method:
            Print the result
        Params:
            raw_cnf: the origin input cnf
        """
        pass

    def solve(self):
        while True:
            # do BCP process
            self.unit_propagate()
            # do "conflict analysis" process
            if self.detect_false_clause():
                if self.now_decision_level == 0:
                    return False
                new_clause, back_level = self.conflict_analyze()
                self.cnf.clause_list.append(new_clause)
                # do BACKTRACK process
                self.backtrack(back_level)
            else:
                if not self.unknown_variable_exists():
                    return True
                # do DECIDE process
                self.make_new_decision_level()
                new_unknown_literal = self.get_new_unknown_literal()
                self.cnf = self.cnf.append(new_unknown_literal)


if __name__ == "__main__":
    cnf = cnf_parse("./raw/test.cnf")
    raw_cnf = deepcopy(cnf)
    solver = SatSolver(cnf)
    # solver.solve()
    # solver.print_result(raw_cnf=raw_cnf)
