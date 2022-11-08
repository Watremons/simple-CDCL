# Standard lib
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
        self.node_index = 0
        self.cnf = cnf
        self.trail = Trail(node_list=[])
        self.variable_to_node = dict()
        self.assignments = dict()
        self.now_decision_level = 0
        # Use assignments to record the variable to assigned node
        self.assignments = dict()
        self.answer=None
        for i in range(1,cnf.variable_num+1):
            self.assignments[i] = None

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

    def get_value(self, variable) :
        """
        Method:
            Get the value of a variable
        """
        if variable in self.assignments:
            return self.assignments[variable]
        else:
            return None

    def find_unit_clause(self) -> tuple[Literal, Clause]:
        """
        Method:
            check if there is unit clause in cnf
        """
        for index in range(len(self.cnf.clause_list)):
            clause=self.cnf.clause_list[index]
            len_clause = len(clause.literal_list)
            #the number of unassigned literals
            num_undefined = 0
            #the number of literals assigned False
            num_false = 0
            #the unassigned literal
            undefined_literal = None
            for literal in clause.literal_list:
                value = self.get_value(literal.variable)
                if value == False:
                    num_false += 1
                elif value == None:
                    undefined_literal = literal
                    num_undefined += 1
            if num_undefined == 1:
                return undefined_literal, index
        return None, None

    def unit_propagate(self):
        """
        Method:
            do unit propagate
        """
        # the literal used to do unit propagate
        literal = None
        while True:
            literal, clause_index = self.find_unit_clause()
            if literal == None:
                #there is no unit clause
                break
            self.set_value(literal)
            self.append_node_to_current_level(literal, clause_index)
        self.update_clause_value()

    #TODO ：在迹中添加结点
    def append_node_to_current_level(self, literal, clause_index):
        node=Node(variable=literal.variable, value=self.get_value(literal.variable), reason=clause_index, level=self.now_decision_level, index=self.node_index)
        self.node_index+=1
        self.trail.node_list.append(node)
        pass

    def update_clause_value(self):  # 更新子句的值
        """
        Method:
            Update the value of each clause
        """
        for clause in self.cnf.clause_list:
            len_clause = len(clause.literal_list)
            #the number of Ture literal
            num_true = 0
            #the number of False literal
            num_false = 0
            for literal in clause.literal_list:
                r = self.get_value(literal.variable)
                if r == True:
                    num_true += 1
                elif r == False:
                    num_false += 1
            if num_true >= 1:  # 至少有一个文字取真
                clause.value = True  # 则子句取真
            elif num_false == len_clause:  # 所有文字取假（冲突）
                clause.value = False  # 则子句取假

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
        conflict_clause = Clause(literal_list=reason_literal_list,literal_num=len(reason_literal_list))

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

    def set_value(self, literal):
        """
        Method:
            Set the value of literal
        """
        if literal.variable in self.assignments :
            self.assignments[literal.variable]= literal.sign

    def backtrack(self, back_level: int) -> None:
        """
        Method:
            Use the cnf which adds the study clause and backtrack decision level to do backtrack
            1.Set now decision level to the backtrack level
            2.Remove all nodes whose level is greater than back_level from trail
        Params:
            back_level: the decision level that the solver need to backtrack to
        """
        self.now_decision_level = back_level
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

    def decide(self):
        """
        Method:
            Select a variable to assign value
        """
        # Sequential traversal the cnf to find an unassigned literal
        for clause in self.cnf.clause_list:
            for literal in clause.literal_list:
                value=self.get_value(literal.variable)
                if value == None:
                    return literal
        return None

    def unassigned_variable_exists(self):
        """
        Method:
            Check if there is still unassigned variable existing
        """
        for i in range(1,cnf.variable_num+1):
            if self.assignments[i] == None:
                return True
        return False


    def detect_false_clause(self):
        # TODO: Add the conflict clause to trail if detecting a false clause
        pass

    def print_result(self, raw_cnf):
        """
        Method:
            Print the result
        """
        print(raw_cnf)
        print(self.answer)
        for i in range(1,cnf.variable_num+1):
            #print( "{"+str(i)+":"+str(self.assignments[i])+"}",end=' ')
            print( f'{i}:{self.assignments[i]}',end=' ')
        print()

    def solve(self):
        while True:
            # do BCP process
            self.unit_propagate()
            # do "conflict analysis" process
            if self.detect_false_clause():
                if self.now_decision_level == 0:
                    self.answer="UNSAT"
                    return
                new_clause, back_level = self.conflict_analyze()
                self.cnf.clause_list.append(new_clause)
                # do BACKTRACK process
                self.backtrack(back_level)
            else:
                if not self.unassigned_variable_exists():
                    self.answer="SAT"
                    return
                # do DECIDE process
                self.now_decision_level += 1
                new_unassigned_literal = self.decide()
                if new_unassigned_literal:
                    self.set_value(new_unassigned_literal)
                    self.append_node_to_current_level(new_unassigned_literal, None)


if __name__ == "__main__":
    cnf = cnf_parse("./raw/test.cnf")
    #print(cnf)
    raw_cnf = deepcopy(cnf)
    solver = SatSolver(cnf)
    solver.solve()
    solver.print_result(raw_cnf=raw_cnf)
    print(solver.trail)
