from models import Literal, Clause, Cnf


def cnf_parse(file_path: str) -> Cnf:
    """
    Method:
        parse the cnf file to Cnf
    """
    file_content = []
    with open(file_path) as f:
        while True:
            line = f.readline()
            # Skip the comment lines which starts with 'c' and delete '\n' at the end
            if not line:
                break
            elif line.startswith('c'):
                pass
            else:
                file_content.append(line.rstrip('\n'))
        f.close()

    # Get the first line after comment, starts with p cnf
    literal_num = 0
    clause_num = 0
    params = file_content[0].split(' ')
    assert params[0] == 'p' and params[
        1] == "cnf", "InputError: Context need to start with 'p' and 'cnf'"

    literal_num = int(params[2])
    clause_num = int(params[3])

    assert clause_num == (
        len(file_content) -
        1), "InputError: The lines of context is not equal to nclause"
    # Read every line as a clause
    clause_list = []
    for line_index in range(1, clause_num):
        raw_literal_list = file_content[line_index].split(' ')
        literal_list = []
        for raw_literal in raw_literal_list:
            if raw_literal.startswith('-'):
                # Handle a "NOT" literal
                variable = int(raw_literal.lstrip('-'))
                sign = True
                literal = variable + literal_num
            else:
                # Handle a literal
                variable = int(raw_literal)
                sign = False
                literal = variable
            if variable == 0:
                break
            literal_list.append(Literal(variable=variable, sign=sign, literal=literal))
        clause_list.append(Clause(literal_list=literal_list))
    return Cnf(clause_list=clause_list, literal_num=literal_num)


if __name__ == "__main__":
    cnf = cnf_parse("./raw/test.cnf")
    print('cnf', cnf)
