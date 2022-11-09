from models import Node, Trail
from parse import cnf_parse
from solver import SatSolver

if __name__ == "__main__":
    now_decision_level = 2
    variable_to_node = dict()

    trail = Trail(node_list=[
        Node(variable=1, value=True, reason=None, level=1, index=0),
        Node(variable=2, value=False, reason=0, level=1, index=1),
        Node(variable=3, value=True, reason=1, level=1, index=2),
        Node(variable=4, value=False, reason=2, level=1, index=3),
        Node(variable=5, value=True, reason=3, level=1, index=4),
        Node(variable=6, value=False, reason=None, level=2, index=5),
        Node(variable=7, value=False, reason=4, level=2, index=6),
        Node(variable=8, value=True, reason=5, level=2, index=7),
        Node(variable=9, value=False, reason=6, level=2, index=8),
        Node(variable=10, value=True, reason=7, level=2, index=9),
        Node(variable=11, value=True, reason=8, level=2, index=10),
        Node(variable=12, value=False, reason=9, level=2, index=11),
        Node(variable=None, value=True, reason=10, level=2, index=12),
    ])

    node_list = []
    new_node = Node(variable=1, value=True, reason=None, level=1, index=0)
    node_list.append(new_node)
    variable_to_node[1] = new_node
    new_node = Node(variable=2, value=False, reason=0, level=1, index=1)
    node_list.append(new_node)
    variable_to_node[2] = new_node
    new_node = Node(variable=3, value=True, reason=1, level=1, index=2)
    node_list.append(new_node)
    variable_to_node[3] = new_node
    new_node = Node(variable=4, value=False, reason=2, level=1, index=3)
    node_list.append(new_node)
    variable_to_node[4] = new_node
    new_node = Node(variable=5, value=True, reason=3, level=1, index=4)
    node_list.append(new_node)
    variable_to_node[5] = new_node
    new_node = Node(variable=6, value=False, reason=None, level=2, index=5)
    node_list.append(new_node)
    variable_to_node[6] = new_node
    new_node = Node(variable=7, value=False, reason=4, level=2, index=6)
    node_list.append(new_node)
    variable_to_node[7] = new_node
    new_node = Node(variable=8, value=True, reason=5, level=2, index=7)
    node_list.append(new_node)
    variable_to_node[8] = new_node
    new_node = Node(variable=9, value=False, reason=6, level=2, index=8)
    node_list.append(new_node)
    variable_to_node[9] = new_node
    new_node = Node(variable=10, value=True, reason=7, level=2, index=9)
    node_list.append(new_node)
    variable_to_node[10] = new_node
    new_node = Node(variable=11, value=True, reason=8, level=2, index=10)
    node_list.append(new_node)
    variable_to_node[11] = new_node
    new_node = Node(variable=12, value=False, reason=9, level=2, index=11)
    node_list.append(new_node)
    variable_to_node[12] = new_node
    new_node = Node(variable=None, value=True, reason=10, level=2, index=12)
    node_list.append(new_node)

    cnf = cnf_parse("./raw/test2.cnf")
    solver = SatSolver(cnf)
    solver.now_decision_level = now_decision_level
    solver.trail = trail
    solver.variable_to_node = variable_to_node
    study_clause, back_level = solver.conflict_analyze()
    print("study_clause", study_clause)
    print("back_level", back_level)
    solver.cnf.clause_list.append(study_clause)
    # do BACKTRACK process
    solver.backtrack(back_level)
    for node in solver.trail.node_list:
        print(node)
    for key, node in solver.variable_to_node.items():
        print(key, node)
