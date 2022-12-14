
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
    print("variable", variable)
    print("conflict_clause", conflict_clause)
    print("to_resolute_clause", to_resolute_clause)
    # merge two clause and remove duplicates
    result_clause_literal_set = set(conflict_clause.literal_list + to_resolute_clause.literal_list)
    # Delete the target variable
    result_clause_literal_set.discard(Literal(variable, 1, variable))
    result_clause_literal_set.discard(Literal(variable, 0, variable + variable_num))
    # Return the clause
    return Clause(literal_list=list(result_clause_literal_set), _literals_watching_c=[])


if __name__ == "__main__":
    list1 = [
        Literal(1, 1, 1),
        Literal(2, 1, 2),
        Literal(3, 1, 3),
        Literal(4, 1, 4),
        Literal(5, 1, 5)
    ]
    list2 = [
        Literal(2, 0, 8),
        Literal(3, 1, 3),
        Literal(4, 1, 4),
        Literal(5, 1, 5),
        Literal(6, 1, 6)
    ]
    all_set = list1+list2
    # full_set = list(OrderedDict.fromkeys(all_set))
    full_set = set(all_set)
    print("all_set")
    for literal in all_set:
        print(literal)
    print("full_set")
    for literal in full_set:
        print(literal)
