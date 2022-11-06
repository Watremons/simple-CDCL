from models import Node, Trail
from models import Clause, Literal


def conflict_analyze(trail: Trail, variable_num: int) -> tuple[Clause, int]:
    """
    Method:
        analyze the trail when cnf have a false clause
        1.Construct the implication graph according to trail
        2.Search UIPs on the graph and get the first one (the first one means the closest UIP to the conflict node)
        3.Divide the nodes to two parts which one has the node that can reach from UIP and another has the rest
        4.Do UIP cut on the edge between the two parts and get the study clause
        5.Record the backtrack decision level
        6.Return
    Return:
        study_clause: the clause which study from the conflict
        backtrack_decision_level: the decision level which need to backtrack
    """
    # Do with self.cnf
    # 1.Construct the implication graph according to trail
    implication_graph = [{"value": True, "outgoing": []} for _ in range(variable_num+1)]
    for decision_level in trail.decision_level_list:
        for node in decision_level.node_list:
            if node.variable is not None:
                implication_graph[node.variable]["value"] = node.value
            if node.reason is not None:
                for start_vertex in node.reason:
                    implication_graph[start_vertex]["outgoing"].append(node.variable)
    # for idx, node in enumerate(implication_graph):
    #     print(idx, node)
    print( Clause(literal_list=[Literal(variable=1, sign=1, literal=1)]), 0)


if __name__ == "__main__":
    trail = Trail(decision_node_list=[
        Node(variable=1, value=True, reason=None, level=1, index=0),
        Node(variable=2, value=False, reason=[13], level=1, index=1),
        Node(variable=3, value=True, reason=[13], level=1, index=2),
        Node(variable=4, value=False, reason=[15], level=1, index=3),
        Node(variable=5, value=True, reason=[2, 4], level=1, index=4),
        Node(variable=6, value=False, reason=None, level=2, index=5),
        Node(variable=7, value=False, reason=[17, 6], level=2, index=6),
        Node(variable=8, value=True, reason=[2, 7], level=2, index=7),
        Node(variable=9, value=False, reason=[20], level=2, index=8),
        Node(variable=10, value=True, reason=[20], level=2, index=9),
        Node(variable=11, value=True, reason=[9, 22], level=2, index=10),
        Node(variable=12, value=False, reason=[22], level=2, index=11),
        Node(variable=None, value=True, reason=[23, 12], level=2, index=12),
    ])

    conflict_analyze(trail=trail, variable_num=12)
