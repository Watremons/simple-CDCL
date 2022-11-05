class Literal:
    '''
    Class:
        Definition of literal
    Attributes:
        variable: variables ranging from 0 to 2n
        sign: sign=1 when the literal is Ture, sign=0 when the literal is False
        literal: literals ranging from 1 to 2n, with negative literals ranging form n+1 to 2n
    Method:
        None
    '''
    def __init__(self, variable: int, sign: int, literal: int) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.variable = variable
        self.sign = sign
        self.literal = literal

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        return str(self.variable) if not self.sign else '-{0}'.format(self.variable)


class Clause:
    '''
    Class:
        Definition of clause
    Attributes:
        literal_list: a list of literals denoted to a disjunctive normal form of them
    Method:
        None
    '''
    def __init__(self, literal_list: list[Literal]) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.literal_list = literal_list

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        for index, literal in enumerate(self.literal_list):
            description += "x{0}".format(
                literal.variable) if not literal.sign else "-x{0}".format(
                    literal.variable)
            if index != len(self.literal_list) - 1:
                description += "V"
        return description


class Cnf:
    '''
    Class:
        Definition of Cnf
    Attributes:
        clause_list: a list of clauses denoted to a conjunctive normal form of them
        clause_num= the number of clauses
        variable_num: the number of variables
    Method:
        None
    '''
    def __init__(self, clause_list: list[Clause], clause_num: int, variable_num: int) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.clause_list = clause_list
        self.clause_num = clause_num
        self.variable_num = variable_num

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = "clause_num={0},variable_num={1}".format(self.clause_num, self.variable_num)
        for index, clause in enumerate(self.clause_list):
            description += "({0})".format(clause.__str__())
            if index != len(self.clause_list) - 1:
                description += "^"
        return description


class Node:
    '''
    Class:
        Node of implication graph
    Attributes:
        variable: variable in node
        value: the value of the decided variable
        reason: the reason why this variable is assigned, which is either assigned by decide or assigned by other clauses
        level: the decision level of this node
    Method:
        None
    '''
    def __init__(self, variable, value, reason, level: int) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.variable = variable
        self.value = value
        self.reason = reason
        self.level = level

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        description += "variable: {0}\n".format(self.variable)
        description += "value: {0}\n".format(self.value)
        description += "reason: {0}\n".format(self.reason)
        description += "level: {0}\n".format(self.level)
        return description


class DecisionLevel:
    """
    Class:
        Definition of Decision Level, which is created when decide the value of a literal
    Attributes:
        node_list: the list of node included in this decision level
        level: the decision level
    Method:
        None
    """
    def __init__(self, node_list: list[Node], level: int) -> None:
        """
        Method:
            Constructed Function
        """
        self.node_list = node_list
        self.level = level

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        description += "Decision Level {0}\n".format(self.level)
        for index, node in enumerate(self.node_list):
            description += "\tNode {0}:\n".format(index)
            description += "\tvalue: {0}\n".format(node.value)
            description += "\treason: {0}\n".format(node.reason)
            description += "\tlevel: {0}\n".format(node.level)
        return description


class Trail:
    """
    Class:
        Definition of Trail, which is stored several decision levels linearly
    Attributes:
        decision_level_list: a list of decision level which are included in a trail
    Method:
        None
    """
    def __init__(self, decision_level_list: list) -> None:
        """
        Method:
            Constructed Funcion
        """
        self.decision_level_list = decision_level_list

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        description += "Trail:"
        for decision_level in self.decision_level_list:
            for node in decision_level.node_list:
                description += "{0}\t{1}\t{2}\n".format(
                    node.literal, node.reason, node.level)
        return description


if __name__ == "__main__":
    n = 1
    print(type(n))
