
from models import Clause, Literal


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


def to_literal(variable: int, sign: int, variable_num: int) -> int:
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


def resolute_clause(conflict_clause: Clause, to_resolute_clause: Clause, variable: int, variable_num: int) -> Clause:
    """
    Method:
        resolute two clanse and return a result clause
        for the clause A [1, 2, 4] and clause B[-1, 2, 3], the function resolute the two clause and return [2, 3, 4]
    Params:
        conflict_clause: clause A
        to_resolute_clause: clause B
        variable: the variable to be resolute in both A and B
        variable_num: the variable num in the cnf
    Return:
        the result clause
    """
    # merge two clause and remove duplicates
    result_clause_literal_set = set(conflict_clause.literal_list + to_resolute_clause.literal_list)
    # Delete the target variable
    result_clause_literal_set.remove(Literal(variable, 1, variable))
    result_clause_literal_set.remove(Literal(variable, 0, variable + variable_num))
    # Return the clause
    return Clause(literal_list=list(result_clause_literal_set))


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
    all_set = set(list1+list2)
    for literal in all_set:
        print(literal)
    all_set.remove(Literal(2, 1, 2))
    for literal in all_set:
        print(literal)
