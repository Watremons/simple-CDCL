# Customized lib
from models import Literal, Clause, Cnf, PriorityQueue
from models import Node, Trail
from utils import resolute_clause, to_literal, to_variable
import queue


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
    def __init__(self, conflict_threshold: int, decider: str):
        """
        Method:
            Constructed Function
        """
        self.node_index = 0
        self.trail = Trail(node_list=[])
        self.variable_to_node = dict()
        self.assignments = dict()
        self.now_decision_level = 0
        self._clauses_watched_by_l = []
        # Data used in heuristic decide
        """
        Heuristic Decide:
            1.init score list and priority list when parse the .cnf file
            2.pop greatest element from priority list when making a decision or BCP
            3.modified the score list when conflicts happen
            4.add elements according to score list when backtrack
        """
        # Decider type
        self.decider = decider
        # score for each variables and size 2*variable_num+1 in VSIDS
        self.literal_score_list = []
        # score for each literals and size variable_num+1 in MINISAT
        self.variable_score_list = []
        # last value for each variables
        # size variable_num+1 in MINISAT
        self.phase = []
        # Extra score for each conflicts
        self.decide_conflict_score = 1
        # Increment of conflict score for each conflicts
        self.score_increment = 0
        # A priority queue for variable ordered by variable score
        self.decide_priority_queue = None

        # Data used in heuristic restart
        self.conflict_num = 0
        self.restart_num = 0
        self.conflict_threshold = conflict_threshold
        # Use assignments to record the variable to assigned node
        self.assignments = dict()
        self.answer = None

    def cnf_parse(self, file_path: str) -> Cnf:
        """
        Method:
            Parse the .cnf file to a Cnf instance
        Params:
            file_path: the file path of .cnf file
        Return:
            cnf: the cnf extracted from .cnf file
        """
        file_content = []
        with open(file_path) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                elif line.startswith('c'):
                    # Skip the comment lines which starts with 'c' and delete '\n' at the end
                    pass
                elif line.startswith('p'):
                    # Get the first line after comment, starts with p cnf
                    word_list = line.split(' ')
                    assert word_list[1] == "cnf", "InputError: Context need to start with 'p' and 'cnf'"
                    variable_num = int(word_list[2])
                    clause_num = int(word_list[3])
                else:
                    file_content.append(line.rstrip('\n'))
            f.close()

        assert variable_num is not None and clause_num is not None, "InputError: Context need to start with 'p' and 'cnf'"
        assert clause_num == (
            len(file_content)
        ), "InputError: The lines of context <int:{file_content}> is not equal to clause <int:{clause_num}>".format(
            file_content=len(file_content), clause_num=clause_num)

        # Init the score used in decider
        if self.decider == "VSIDS":
            self.literal_score_list = [0 for _ in range(variable_num*2 + 1)]
        elif self.decider == "MINISAT":
            self.variable_score_list = [0 for _ in range(variable_num + 1)]
            self.phase = [False for _ in range(variable_num + 1)]

        #initial the _clauses_watched_by_l list:
        _clauses_watched_by_l=[]
        for i in range(2*variable_num+1):
            lst=list()
            _clauses_watched_by_l.append(lst)

        # Read every line as a clause
        clause_list = []
        for line_index in range(clause_num):
            raw_literal_list = file_content[line_index].split(' ')
            raw_literal_list = raw_literal_list[:-1]
            literal_list = []
            for raw_literal in raw_literal_list:
                if raw_literal.startswith('-'):
                    # Handle a negative literal
                    variable = int(raw_literal.lstrip('-'))
                    sign = False
                    literal = variable + variable_num
                else:
                    # Handle a positive literal
                    variable = int(raw_literal)
                    sign = True
                    literal = variable
                literal_list.append(Literal(variable=variable, sign=sign, literal=literal))

                # Record the score for specific decider
                if self.decider == "VSIDS":
                    self.literal_score_list[literal] += 1
                elif self.decider == "MINISAT":
                    self.variable_score_list[variable] += 1

            # 2- literal watching
            _literals_watching_c = []
            if len(literal_list) == 1:
                # If this is a unary clause, then that unary literal has to be set True and so we treat it as a special case
                _literals_watching_c = [literal_list[0]]
                _clauses_watched_by_l[literal_list[0].literal].append(line_index)
            else:
                # If this is not a unary clause
                _literals_watching_c = [literal_list[0], literal_list[1]]
                _clauses_watched_by_l[literal_list[0].literal].append(line_index)
                _clauses_watched_by_l[literal_list[1].literal].append(line_index)

            clause_list.append(Clause(literal_list=literal_list,_literals_watching_c=_literals_watching_c))

        # Set the cnf for solver
        self.cnf = Cnf(clause_list=clause_list, clause_num=clause_num, variable_num=variable_num)
        self._clauses_watched_by_l=_clauses_watched_by_l
        for i in range(1, self.cnf.variable_num+1):
            self.assignments[i] = None

        # Set the decider params for solver
        if self.decider == "VSIDS":
            self.decide_priority_queue = PriorityQueue(self.literal_score_list)
            self.score_increment = 0.75
        elif self.decider == "MINISAT":
            self.decide_priority_queue = PriorityQueue(self.variable_score_list)
            self.score_increment = 0.85

        return self.cnf

    def test_print_2watcing(self):
        #TODO 测试_clauses_watched_by_l 文字->监控的子句
        for j in range(1,self.cnf.variable_num*2+1):
            print(j,self._clauses_watched_by_l[j])

        #TODO 测试 子句->监控子句的两个文字
        for j in range(self.cnf.clause_num):
            print(j,end=' ')
            for i in self.cnf.clause_list[j]._literals_watching_c:
                print(i.literal,end=' ')
            print()

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
            #print("冲突的文字",conflict_variable)
            #print("现在的迹:" ,self.trail)
            variable_node = self.variable_to_node[conflict_variable]
            if variable_node.level == conflict_level:
                count += 1
                if max_index < variable_node.index:
                    max_index = variable_node.index
                    max_index_node = variable_node

        return count == 1, max_index_node

    def get_value(self, literal):
        """
        Method:
            Get the value of a variable
        """
        if literal.variable in self.assignments:
            if self.assignments[literal.variable] is None:
                return None
            elif literal.sign == self.assignments[literal.variable]:
                return True
            else:
                return False
        else:
            return None

    def find_unit_clause(self) -> tuple[Literal, Clause]:
        """
        Method:
            check if there is unit clause in cnf
        """
        '''
        for index in range(len(self.cnf.clause_list)):
            if (len(self.cnf.clause_list[index]._literals_watching_c)==1):
                return self.cnf.clause_list[index]._literals_watching_c[0],index
        return None, None
'''

        for index in range(len(self.cnf.clause_list)):
            clause = self.cnf.clause_list[index]
            if clause.value is not None and clause.value:
                continue
            # len_clause = len(clause.literal_list)
            # the number of unassigned literals
            num_undefined = 0
            # the number of literals assigned False
            num_false = 0
            # the unassigned literal
            undefined_literal = None
            for literal in clause.literal_list:
                value = self.get_value(literal)
                if value is None:
                    undefined_literal = literal
                    num_undefined += 1
                elif not value:
                    num_false += 1
            if num_undefined == 1:
                return undefined_literal, index
        return None, None

    def unit_propagate_1(self):
        """
        Method:
            do unit propagate
        """
        # the literal used to do unit propagate
        literal = None
        while True:
            literal, clause_index = self.find_unit_clause()
            if literal is None:
                # there is no unit clause
                break
            if self.decider == "VSIDS":
                self.decide_priority_queue.remove(literal.variable)
                self.decide_priority_queue.remove(
                    to_literal(
                        variable=literal.variable,
                        sign=False,
                        variable_num=self.cnf.variable_num
                    )
                )
            if self.decider == "MINISAT":
                self.decide_priority_queue.remove(literal.variable)
                self.phase[literal.variable] = literal.sign
            self.set_value(literal, literal.sign)
            self.append_node_to_current_level(literal, clause_index)

    def unit_propagate(self, unit_clause):
        #print("单位传播:", end=' ')
        literal = None

        dic = {}
        for i in range(self.cnf.variable_num + 1):
            dic[i] = -1

        i = 0
        while (i < len(unit_clause)):
            if dic[unit_clause[i][0].variable] == 1:
                unit_clause.remove(unit_clause[i])
            else:
                dic[unit_clause[i][0].variable] = 1
                i += 1

        #while True:
        #    literal, clause_index = self.find_unit_clause()
        for item in unit_clause:
            literal, clause_index = item
            if literal is None:
                # there is no unit clause
                break
            #print("文字", literal, "子句", clause_index, end=', ')
            if self.decider == "VSIDS":
                self.decide_priority_queue.remove(literal.variable)
                self.decide_priority_queue.remove(
                    to_literal(
                        variable=literal.variable,
                        sign=False,
                        variable_num=self.cnf.variable_num
                    )
                )
                # print(self.literal_score_list)
                # print(self.decide_priority_queue)
            if self.decider == "MINISAT":
                self.decide_priority_queue.remove(literal.variable)
                self.phase[literal.variable] = literal.sign
            unit_c = self.set_value(literal, literal.sign)

            for i in unit_c:
                if dic[i[0].variable] == -1:
                    unit_clause.append(i)
                    dic[i[0].variable] = 1
            self.append_node_to_current_level(literal, clause_index)
        #print()
        #print("一一比较:", end=' ')
        #for i in unit_clause:
            #print("文字", i[0], "子句", i[1], end=', ')

        #print()

    def append_node_to_current_level(self, literal, reason):
        """
        Method:
            Append new node to trail
        """
        #print("加入迹",literal.variable,self.now_decision_level)
        node = Node(variable=literal.variable, value=self.assignments[literal.variable], reason=reason, level=self.now_decision_level, index=self.node_index)
        self.trail.node_list.append(node)
        self.variable_to_node[literal.variable] = node
        self.node_index += 1

    def update_clause_value(self):  # 更新子句的值
        """
        Method:
            Update the value of each clause
        """
        for index in range(self.cnf.clause_num):
            self.update_single_clause_value(index)

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

        # reason_literal_list = []
        # for reason_literal in conflict_node.reason:
        #     variable, sign = to_variable(reason_literal, self.cnf.variable_num)
        #     reason_literal_list.append(Literal(variable=variable, sign=sign, literal=reason_literal))
        # conflict_clause = Clause(literal_list=reason_literal_list)
        conflict_clause = self.cnf.clause_list[conflict_node.reason]

        # 2.Check the conflict clause has only one literal at conflict level
        # if not, use the clause at conflict level to resolute excess literals
        while True:
            flag, latest_conflict_level_node = self.is_study_clause(conflict_clause, last_decision_level)
            if flag:
                break
            to_resolute_clause = self.cnf.clause_list[latest_conflict_level_node.reason]

            conflict_clause = resolute_clause(
                conflict_clause=conflict_clause,
                to_resolute_clause=to_resolute_clause,
                variable=latest_conflict_level_node.variable,
                variable_num=self.cnf.variable_num
            )

        study_clause = conflict_clause
        # Modify the heuristic decide related data
        if self.decider == "VSIDS":
            for study_literal in study_clause.literal_list:
                self.literal_score_list[study_literal.literal] += self.decide_conflict_score
                self.decide_priority_queue.increase_priority(study_literal.literal, self.decide_conflict_score)
            self.decide_conflict_score += self.score_increment

        if self.decider == "MINISAT":
            for study_literal in study_clause.literal_list:
                self.variable_score_list[study_literal.variable] += self.decide_conflict_score
                self.decide_priority_queue.increase_priority(study_literal.variable, self.decide_conflict_score)
            self.decide_conflict_score /= self.score_increment

        # print(self.literal_score_list)
        # print(self.decide_priority_queue)
        # 3.Record the backtrack decision level
        if len(conflict_clause.literal_list) == 1:
            # return to level 0 if study clause has only one literal
            backtrack_decision_level = 0
        else:
            # return to target level if study clause has more than one literal
            study_clause_decision_level_set = set()
            for reason_literal in conflict_clause.literal_list:
                study_clause_decision_level_set.add(self.variable_to_node[reason_literal.variable].level)
            lst = list(study_clause_decision_level_set)
            lst.sort(reverse=False)
            backtrack_decision_level = lst[-2]
        # 4.set 2 watching literal for the study_clause
        literal_list=study_clause.literal_list
        _literals_watching_c = []
        if len(literal_list) == 1:
            # If this is a unary clause, then that unary literal has to be set True and so we treat it as a special case
            _literals_watching_c = [literal_list[0]]
            self._clauses_watched_by_l[literal_list[0].literal].append(self.cnf.clause_num)
        else:
            # If this is not a unary clause
            _literals_watching_c = [literal_list[0], literal_list[1]]
            self._clauses_watched_by_l[literal_list[0].literal].append(self.cnf.clause_num)
            self._clauses_watched_by_l[literal_list[1].literal].append(self.cnf.clause_num)
        study_clause._literals_watching_c=_literals_watching_c
        # 5.Return
        return study_clause, backtrack_decision_level

    def update_single_clause_value(self, index):
        clause = self.cnf.clause_list[index]
        len_clause = len(clause.literal_list)
        # the number of Ture literal
        num_true = 0
        # the number of False literal
        num_false = 0
        for literal in clause.literal_list:
            r = self.get_value(literal)
            if r is None:
                continue
            elif r:
                num_true += 1
            elif not r:
                num_false += 1
        if num_true >= 1:  # 至少有一个文字取真
            clause.value = True  # 则子句取真
        elif num_false == len_clause:  # 所有文字取假（冲突）
            clause.value = False  # 则子句取假
        else:
            clause.value = None

    def set_value(self, literal, value):
        """
        Method:
            Set the value of literal and update the value of clause
        """
        #print("set_value",literal.variable,value,"决策层",self.now_decision_level)
        if literal.variable in self.assignments:
            self.assignments[literal.variable] = value
        #2 watching literal
        _0_literal=literal.variable
        _1_literal=literal.variable
        if value == False:
            _1_literal = literal.variable+self.cnf.variable_num
        elif value==True:
            _0_literal = literal.variable+self.cnf.variable_num
        #print(literal.variable,value)
        unit_clause = []
        conflict_clause = -1
        #print(" 0文字",_0_literal,"监控的子句",self._clauses_watched_by_l[_0_literal])
        _0_list=list(self._clauses_watched_by_l[_0_literal])
        for index in _0_list:
            self.update_single_clause_value(index)
            if self.cnf.clause_list[index].value == True:
                #print("  不用考虑的真子句",index)
                #if the clause is already True, it need not be token attention
                continue
            #print("  ",index,"监视的还未赋值的子句")
            if len(self.cnf.clause_list[index]._literals_watching_c)!=1:
                #if the clause is not unit clause, try to find another rational watching literal
                new_watching_literal=None
                for l in self.cnf.clause_list[index].literal_list:
                    if l not in self.cnf.clause_list[index]._literals_watching_c and self.get_value(l) !=False:
                        # set this literal as the new watching literal
                        new_watching_literal=l
                        break

                if new_watching_literal is not None:
                    #print("   新的监视文字",new_watching_literal)
                    # set the new_watching_literal as the new watching literal
                    for l in self.cnf.clause_list[index]._literals_watching_c:
                        if l.variable==literal.variable:
                            self.cnf.clause_list[index]._literals_watching_c.remove(l)
                    self.cnf.clause_list[index]._literals_watching_c.append(new_watching_literal)
                    self._clauses_watched_by_l[_0_literal].remove(index)
                    self._clauses_watched_by_l[new_watching_literal.literal].append(index)
                else:
                    #if there is no another rational watching literal, then check the other watching literal
                    other_watching_literal=self.cnf.clause_list[index]._literals_watching_c[0]
                    if other_watching_literal.literal == _0_literal:
                        other_watching_literal=self.cnf.clause_list[index]._literals_watching_c[1]
                    #print("   另一个监视文字",other_watching_literal)
                    if self.assignments[other_watching_literal.variable] is None:
                        # there will be a unit clause
                        unit_clause.append((other_watching_literal,index))
                        #print("    单位字句，赋值",other_watching_literal)
                    elif self.assignments[other_watching_literal.variable] == False:
                        # there will be a conflict clause
                        pass
        #print(" 1文字",_1_literal,"监控的子句",self._clauses_watched_by_l[_1_literal])
        for index in self._clauses_watched_by_l[_1_literal]:
            # set the clause as True for the clause watched by the contrary literal
            self.cnf.clause_list[index].value=True
            #print("  真子句,赋值",index)
        #self.update_clause_value()
        #print(" 此次赋值得出的单位字句",unit_clause, "此次赋值得出的冲突字句",conflict_clause)
        return unit_clause

    def backtrack(self, back_level: int) -> None:
        """
        Method:
            Use the cnf which adds the study clause and backtrack decision level to do backtrack
            1.Set now decision level to the backtrack level
            2.Remove all nodes whose level is greater than back_level from trail
            3.delete the value of some decided variable
            4.update the value of clause
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
                self.trail.node_list.append(last_node)
                # break if no node remain, whose level is greater than back level
                break
            else:
                if last_node.variable is not None:
                    self.variable_to_node.pop(last_node.variable)
                    self.clear_value_of_variable(last_node.variable)
                    #print("清除值",last_node.variable)
                    # Restore the item remove from priority queue
                    if self.decider == "VSIDS":
                        positive_literal = to_literal(variable=last_node.variable, sign=True, variable_num=self.cnf.variable_num)
                        negative_literal = to_literal(variable=last_node.variable, sign=False, variable_num=self.cnf.variable_num)
                        self.decide_priority_queue.push_back(
                            key=positive_literal,
                            value=self.literal_score_list[positive_literal]
                        )
                        self.decide_priority_queue.push_back(
                            key=negative_literal,
                            value=self.literal_score_list[negative_literal]
                        )
                        # print(self.literal_score_list)
                        # print(self.decide_priority_queue)
                    if self.decider == "MINISAT":
                        self.decide_priority_queue.push_back(
                            key=last_node.variable,
                            value=self.variable_score_list[last_node.variable]
                        )
                del last_node
        self.update_clause_value()

    def clear_value_of_variable(self, variable):
        """
        Method:
            Clear the value of variable
        """
        if variable in self.assignments:
            self.assignments[variable] = None

    def decide(self) -> tuple[Literal, bool]:
        """
        Method:
            Select a variable to assign value
        """
        decide_literal = None
        decide_value = None
        if self.decider == "VSIDS":
            # 1.Get the greatest literal and extract the variable
            # 2.Using the variable to do DECIDE
            # 3.Remove the another variable of the literal
            greatest_literal_element = self.decide_priority_queue.pop_front()
            if greatest_literal_element is not None:
                decide_variable, decide_sign = to_variable(
                    literal=greatest_literal_element.key,
                    variable_num=self.cnf.variable_num
                )
                decide_literal = Literal(
                    variable=decide_variable,
                    sign=decide_sign,
                    literal=greatest_literal_element.key
                )
                decide_value = not decide_sign
                self.decide_priority_queue.remove(
                    to_literal(
                        variable=decide_variable,
                        sign=not decide_sign,
                        variable_num=self.cnf.variable_num
                    )
                )
            # print(self.literal_score_list)
            # print(self.decide_priority_queue)
        elif self.decider == "MINISAT":
            # 1.Get the greatest variable
            # 2.Using the variable and sign in phase to do DECIDE
            greatest_variable_element = self.decide_priority_queue.pop_front()
            if greatest_variable_element is not None:
                decide_variable = greatest_variable_element.key
                decide_value = self.phase[decide_variable]
                decide_literal = Literal(
                    variable=decide_variable,
                    sign=decide_value,
                    literal=decide_variable
                )
        elif self.decider == "ORDERED":
            # Sequential traversal the cnf to find an unassigned literal
            for variable in range(1, self.cnf.variable_num+1):
                if self.assignments[variable] is None:
                    decide_literal = Literal(
                        variable=variable,
                        sign=True,
                        literal=variable
                    )
                    decide_value = True
                    break

        return decide_literal, decide_value

    def unassigned_variable_exists(self):
        """
        Method:
            Check if there is still unassigned variable existing
        """
        for i in range(1, cnf.variable_num+1):
            if self.assignments[i] is None:
                return True
        return False

    def detect_conflict_clause(self):
        clause_index = 0
        for clause in self.cnf.clause_list:
            if clause.value is not None and not clause.value:
                return clause_index
            clause_index += 1
        return -1

    def print_result(self, raw_cnf):
        """
        Method:
            Print the result
        """
        #print(raw_cnf)
        print(self.answer,f'the number of restarts is {self.restart_num}')
        #if (self.answer == "SAT"):
        #   for i in range(1, cnf.variable_num+1):
        #        print(f'{i}:{self.assignments[i]}', end=' ')
        #    print()

    def append_conflict_node_to_trail(self, conflict_clause_num):
        """
        Method:
            Append a conflict node to trail
        """
        node = Node(variable=None, value=True, reason=conflict_clause_num,
                    level=self.now_decision_level, index=self.node_index)
        self.trail.node_list.append(node)
        self.node_index += 1

    def solve(self):
        self.unit_propagate_1()
        while True:
            #self.test_print_2watcing()
            unit_clause = []
            # do "conflict analysis" process
            conflict_clause_num = self.detect_conflict_clause()
            if conflict_clause_num != -1:
                if self.now_decision_level == 0:
                    self.answer = "unSAT"
                    return
                # add a conflict node to trail
                self.append_conflict_node_to_trail(conflict_clause_num)
                new_clause, back_level = self.conflict_analyze()
                #print("冲突子句",new_clause,"回溯层",back_level)
                self.cnf.clause_list.append(new_clause)
                self.cnf.clause_num += 1
                # Count the number of conflicts and restart
                self.conflict_num += 1
                if self.conflict_num == self.conflict_threshold:
                    # do th restart
                    self.conflict_num = 0
                    self.restart_num += 1
                    back_level = 0
                # do BACKTRACK process
                self.backtrack(back_level)
                self.unit_propagate_1()
            else:
                if not self.unassigned_variable_exists():
                    self.answer = "SAT"
                    return
                # do DECIDE process
                self.now_decision_level += 1
                #print("decide元素",end='')
                new_unassigned_literal, decide_value = self.decide()
                if new_unassigned_literal:
                    unit_clause = self.set_value(new_unassigned_literal, decide_value)
                    #print("set返回",end=':')
                    #for item in unit_clause:
                        #print("文字",item[0].variable,"子句",item[1],end=',')
                    #print()
                    self.append_node_to_current_level(new_unassigned_literal, None)
                self.unit_propagate(unit_clause)
                #self.unit_propagate(unit_clause)


if __name__ == "__main__":
    heuristic_decider = ["ORDERED","VSIDS","MINISAT"]
    conflict_threshold = 9

    for i in range(3):
        for j in ["./raw/test2.cnf","./raw/test7.cnf"]:
            solver = SatSolver(
                conflict_threshold=conflict_threshold,
                decider=heuristic_decider[i]
            )
            cnf = solver.cnf_parse(j)
            raw_cnf = str(cnf)
            solver.solve()
            solver.print_result(raw_cnf=raw_cnf)
            #print()