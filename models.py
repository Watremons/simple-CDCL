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
    def __init__(self, variable: int, sign: int) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.variable = variable
        self.sign = sign

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        return self.variable

class Clause:
    '''
    Class:
        Definition of literal
    Attributes:
        literalList: a list of literals denoted to a disjunctive normal form of them
    Method:
        None
    '''
    def __init__(self, literalList: list[Literal]) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.literalList = literalList

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        for index, literal in enumerate(self.literalList):
            description += "x{0}".format(literal)
            if index != len(self.literalList):
                description += "∪"
        return description

class Cnf:
    '''
    Class:
        Definition of Cnf
    Attributes:
        clauseList: a list of clauses denoted to a conjunctive normal form of them
    Method:
        None
    '''
    def __init__(self, clauseList: list[Clause], literalNum: int) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.clauseList = clauseList
        self.literalNum = literalNum

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        for index, clause in enumerate(self.clauseList):
            description += "({0})".format(clause.__str__())
            if index != len(self.literalList):
                description += "∩"
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
        nodeList: the list of node which are included in this decision level
        level: the level number of a decision level
    Method:
        None
    """

    def __init__(self, nodeList: list[Node], level: int) -> None:
        """
        Method:
            Constructed Function
        """
        self.nodeList = nodeList
        self.level = level

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        description += "Decision Level {0}\n".format(self.level)
        for index, node in enumerate(self.nodeList):
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
        decisionLevelList: a list of decision level which are included in a trail
    Method:
        None
    """

    def __init__(self, decisionLevelList: list) -> None:
        """
        Method:
            Constructed Funcion
        """
        self.decisionLevelList = decisionLevelList

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        description += "Trail:"
        for decisionLevel in self.decisionLevelList:
            for node in decisionLevel.nodeList:
                description += "{0}\t{1}\t{2}\n".format(node.literal, node.reason, node.level)

if __name__ == "__main__":
    n = 1
    print(type(n))
