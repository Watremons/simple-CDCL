from copy import deepcopy

# Customized lib
from models import Literal, Clause, Cnf
from models import Node, Trail
from parse import cnf_parse
from utils import resolute_clause, to_clause, to_literal, to_variable

from SatSolver

if __name__ == "__main__":
    cnf = cnf_parse("./raw/test.cnf")
    raw_cnf = deepcopy(cnf)
    solver = SatSolver(cnf)
    # solver.solve()
    # solver.print_result(raw_cnf=raw_cnf)