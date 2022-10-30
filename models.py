class Literal:
    '''
    Class:
        Definition of literal
    Attributes:
        variable: a num of variable whose value is from 0 to 2n-1. If value is from n to 2n-1, that means this variable is a "Not"
        sign: -1 when the variable is "Not"
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
        Definition of literal
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
            description += "x{0}".format(literal.variable) if not literal.sign else "-x{0}".format(literal.variable) 
            if index != len(self.literal_list)-1:
                description += "V"
        return description

class Cnf:
    '''
    Class:
        Definition of Cnf
    Attributes:
        clause_list: a list of clauses denoted to a conjunctive normal form of them
    Method:
        None
    '''
    def __init__(self, clause_list: list[Clause], literal_num: int) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.clause_list = clause_list
        self.literal_num = literal_num

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        for index, clause in enumerate(self.clause_list):
            description += "({0})".format(clause.__str__())
            if index != len(self.clause_list)-1:
                description += "^"
        return description
class Node:
    '''
    Class:
        Node of implication graph
    Attributes:
        literal: literal in node, which means this literal is assigned True
        reason: the reason why this literal is assigned True, which is either decided by user or decided by other clause
        level: the decision level of this node
    Method:
        None
    '''
    def __init__(self, literal, reason, level: int) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.literal = literal
        self.reason = reason
        self.level = level
    
    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        description += "literal: {0}\n".format(self.literal)
        description += "reason: {0}\n".format(self.reason)
        description += "level: {0}\n".format(self.level)
        return description

class DecisionLevel:
    """
    Class:
        Definition of Decision Level, which is created when decide the value of a literal
    Attributes:
        node_list: the list of node which are included in this decision level
        level: the level number of a decision level
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
            description += "\tliteral: {0}\n".format(node.literal)
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
                description += "{0}\t{1}\t{2}\n".format(node.literal, node.reason, node.level)
        return description

if __name__ == "__main__":
    n = 1
    print(type(n))