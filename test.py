from models import Node, DecisionLevel, Trail

if __name__ == "__main__":
    trail = Trail(decision_level_list=[
        DecisionLevel(level=1, node_list=[
            Node(variable=1, value=True, reason=None, level=1),
            Node(variable=2, value=False, reason=[1], level=1),
            Node(variable=3, value=True, reason=[1], level=1),
            Node(variable=4, value=False, reason=[3], level=1),
            Node(variable=5, value=True, reason=[2, 4], level=1),
        ]),
        DecisionLevel(level=2, node_list=[
            Node(variable=6, value=False, reason=None, level=2),
            Node(variable=7, value=False, reason=[5, 6], level=2),
            Node(variable=8, value=True, reason=[2, 7], level=2),
            Node(variable=9, value=False, reason=[8], level=2),
            Node(variable=10, value=True, reason=[8], level=2),
            Node(variable=11, value=True, reason=[9, 10], level=2),
            Node(variable=12, value=False, reason=[10], level=2),
            Node(variable=None, value=True, reason=[11, 12], level=2),
        ])
    ])