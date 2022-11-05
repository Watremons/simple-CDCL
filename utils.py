
from models import Clause, Literal, Node


def to_variable(literal: int, variable_num: int) -> tuple[int, int]:
    """
    Method:
        Trans literal to variable
    Return:
        variable: variable num
        sign: variable sign
    """
    if literal <= variable_num:
        return literal, 1
    else:
        return literal - variable_num, 0


def to_literal(variable: int, sign: int, variable_num: int) -> tuple[int, int]:
    """
    Method:
        Trans variable to literal
    Return:
        literal: literal
    """
    if sign:
        return variable
    else:
        return variable + variable_num


def to_clause(node: Node, variable_num: int) -> Clause:
    """
    Method:
        Trans node to clause
    Return:
        clause: a clause transform from input node
    """
    reason_literal_list = []
    if node.variable is not None:
        reason_literal_list.append(
            Literal(
                variable=node.variable,
                sign=node.value,
                literal=to_literal(variable=node.variable, sign=node.value, variable_num=variable_num)
            )
        )
    for reason_literal in node.reason:
        variable, sign = to_variable(reason_literal, variable_num)
        reason_literal_list.append(Literal(variable=variable, sign=sign, literal=reason_literal))
    return Clause(literal_list=reason_literal_list)

def resolve_clause(conflict_clause: Clause, resolve_clause: Clause, variable: int) -> Clause:
    """
    Method:
        Resolve two clanse and return a result clause
    Return:
        clause: the result clause
    """
    result_clause_literal_set = set(conflict_clause.literal_list + resolve_clause.literal_list)

    result_clause_literal_set.remove()


if __name__ == "__main__":
    list1 = [
        Literal(1, 1, 1),
        Literal(2, 1, 2),
        Literal(3, 1, 3),
        Literal(4, 1, 4),
        Literal(5, 1, 5)
    ]
    list2 = [
        Literal(2, 1, 2),
        Literal(3, 1, 3),
        Literal(4, 1, 4),
        Literal(5, 1, 5),
        Literal(6, 1, 6)
    ]
    for literal in list(set(list1+list2)):
        print(literal)