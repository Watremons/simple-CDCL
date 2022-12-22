
import argparse
import os

from solver import SatSolver


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--decider', type=str, required=True, default="ORDERED", help="decider type ['ORDERED', 'VSIDS', 'MINISAT']")
    parser.add_argument('--threshold', type=int, required=True, default=10000, help="conflict_threshold")
    parser.add_argument('--input_file', type=str, required=True, default="test.cnf", help="input cnf file name")
    args = parser.parse_args()
    return args


def main():
    print("Start")
    args = args_parser()
    base_path = os.path.abspath('.')
    if args.threshold < 0 or args.decider not in ['ORDERED', 'VSIDS', 'MINISAT']:
        print("ParamsError: Please check your args ")
    solver = SatSolver(
        conflict_threshold=args.threshold,
        decider=args.decider
    )
    cnf = solver.cnf_parse(os.path.join(base_path, "raw", args.input_file))
    # solver = SatSolver(
    #     conflict_threshold=10000,
    #     decider="ORDERED"
    # )
    # cnf = solver.cnf_parse(os.path.join(base_path, "raw", "test.cnf"))
    raw_cnf = str(cnf)
    solver.solve()
    solver.stat.restart_times = solver.restart_num
    solver.stat.solver_result = solver.answer
    solver.stat.study_clause_num = len(solver.cnf.clause_list) - solver.stat.clause_num
    solver.print_result(raw_cnf=raw_cnf)
    statistic_str = solver.stat.generate_stat_result()
    stat_path = os.path.join(base_path, "result", solver.stat.output_stat_file_name)
    with open(file=stat_path, mode="w", encoding="utf-8") as f:
        f.write(statistic_str)
    print("Finished successfully")


if __name__ == "__main__":
    main()
