from typing import Union
import heapq


class Literal:
    '''
    Class:
        Definition of literal
    Attributes:
        variable: variables ranging from 1 to 2n
        sign: sign=1 when the literal is True, sign=0 when the literal is False
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
        return str(self.variable) if self.sign else '-{0}'.format(self.variable)

    def __eq__(self, __o: object) -> bool:
        """
        Method:
            Define the equal of two Literal instance
        """
        return self.literal == __o.literal

    def __hash__(self) -> bool:
        """
        Method:
            Define the hash of two Literal instance
        """
        return hash(self.literal)


class Clause:
    '''
    Class:
        Definition of clause
    Attributes:
        literal_list: a list of literals denoted to a disjunctive normal form of them
    Method:
        None
    '''
    def __init__(self, literal_list: list[Literal], _literals_watching_c: list[Literal]) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.literal_list = literal_list
        self.value = None
        #2- literal watching for this clause
        self._literals_watching_c = _literals_watching_c

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        for index, literal in enumerate(self.literal_list):
            description += "x{0}".format(
                literal.variable) if literal.sign else "-x{0}".format(
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
    def __init__(self, clause_list: list[Clause], clause_num: int,
                 variable_num: int) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.clause_list = clause_list
        self.clause_num = clause_num
        self.variable_num = variable_num
        self.answer = ""

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = "clause_num={0},variable_num={1}\n".format(
            self.clause_num, self.variable_num)
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
        variable: variable in node(could be None when node is a conflict)
        value: the value of the decided variable
        reason: the reason why this variable is assigned, which is either assigned by decide or assigned by other clauses
        level: the decision level of this node
        index: the index of node in trail
    Method:
        None
    '''
    def __init__(self, variable: Union[int, None], value: bool,
                 reason: Union[None, int], level: int, index: int) -> None:
        """
        Method:
            Constructed Funtion
        """
        self.variable = variable
        self.value = value
        self.reason = reason
        self.level = level
        self.index = index

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        description += "variable: {0}\t".format(self.variable)
        description += "value:  {0}\t".format(self.value)
        description += "reason:{0}\t".format(self.reason)
        description += "level: {0}\t".format(self.level)
        description += "index: {0}\n".format(self.index)
        return description


class Trail:
    """
    Class:
        Definition of Trail, which is stored several decision levels linearly
    Attributes:
        nodel_list: a list of decision level which are included in a trail
    Method:
        None
    """
    def __init__(self, node_list: list[Node]) -> None:
        """
        Method:
            Constructed Funcion
        """
        self.node_list = node_list

    def __str__(self) -> str:
        """
        Method:
            Formatted print string
        """
        description = ""
        description += "Trail:\n"
        for node in self.node_list:
            description += str(node)
        return description


class PriorityQueueItem:
    """
    Class:
        item in priority queue
    """
    def __init__(self, key: int, value: int) -> None:
        """
        Method:
            Constructed Function
        """
        self.key = key
        self.value = value

    def __lt__(self, other) -> bool:
        return self.value < other.value


class PriorityQueue:
    """
    Class:
        a priority queue ordered by list value
    """
    def __init__(self, queue: list[int]) -> None:
        """
        Method:
            Contructed Function
        """
        raw_queue = []
        for index, element in enumerate(queue[1:], start=1):
            # Push element with minus value to get a greater heap
            heapq.heappush(raw_queue, PriorityQueueItem(key=index, value=-element))
        self.queue = raw_queue

    def pop_front(self) -> Union[PriorityQueueItem, None]:
        """
        Method:
            Get the greatest element at the front of PriorityQueue
        Return:
            element: the greatest element
        """
        if len(self.queue) == 0:
            return None
        return heapq.heappop(self.queue)

    def increase_priority(self, key: int, value: int) -> None:
        """
        Method:
            Modify the priority of item in PriorityQueue by key
        Params:
            key: the key of target item
            value: the increase value of item
        """
        for index in len(self.queue):
            if self.queue[index].key == key:
                self.queue[index].value -= value
                break
        heapq.heapify(self.queue)

    def push_back(self, key: int, value: int) -> None:
        """
        Method:
            Push a new element into PriorityQueue
        Params:
            key: the key of target item
            value: the modified value of item
        """
        heapq.heappush(self.queue, PriorityQueueItem(key=key, value=value))

    def remove(self, key: int) -> None:
        """
        Method:
            Remove a priority queue item by key
        Params:
            key: the key of target priority queue item
        """
        for index, element in enumerate(self.queue):
            if element.key == key:
                del self.queue[index]
                break

    def __str__(self) -> str:
        description = ""
        description += "["
        element_list = []
        for element in self.queue:
            element_list.append("({},{})".format(element.key, element.value))
        description += ",".join(element_list)
        description += "]"
        return description


if __name__ == "__main__":
    value = None
    print(not value)
