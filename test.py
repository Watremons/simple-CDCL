from symtable import Symbol
from typing import Union
from sympy import Symbol
from sympy.logic.boolalg import Not

print(Symbol)
print(Not)
print(Union[Symbol, Not])

def cdcl(cnf):
    cnf_copy = cnf
    while true:
        # do BCP process
        cnf_copy = unitPropagate(cnf, cnf_copy)
        # do "conflict analysis" process
        if hasAFlaseClause(cnf_copy):
            if nowDecisionLevel == 0:
                return False
            new_clause = conflictAnalyze(cnf_copy, cnf)
            cnf = cnf.append(new_clause)
            # do BACKTRACK process 
            back2TargetDecisionLevel()
        else:
            if not valueOfVariablesIsUnknown(cnf_copy):
                return True
            # do DECIDE process
            makeANewDecisionLevel()
            l = getNewLiteralWhoseValueIsUnknown(cnf_copy);
            cnf_copy = cnf_copy.append(l)
