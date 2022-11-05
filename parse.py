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
            elif line.startswith('p'):
                # Get the first line after comment, starts with p cnf
                word_list = line.split(' ')
                assert word_list[1] == "cnf", "InputError: Context need to start with 'p' and 'cnf'"
                variable_num = int(word_list[2])
                clause_num = int(word_list[3])
            else:
                file_content.append(line.rstrip('\n'))
        f.close()

    assert variable_num is not None and clause_num is not None, "InputError: Context need to start with 'p' and 'cnf'"
    assert clause_num == (len(file_content)), "InputError: The lines of context is not equal to clause"
    # Read every line as a clause
    clause_list = []
    for line_index in range(clause_num):
        raw_literal_list = file_content[line_index].split(' ')
        raw_literal_list = raw_literal_list[:-1]
        literal_list = []
        for raw_literal in raw_literal_list:
            if raw_literal.startswith('-'):
                # Handle a "NOT" literal
                variable = int(raw_literal.lstrip('-'))
                sign = True
                literal = variable + variable_num
            else:
                # Handle a literal
                variable = int(raw_literal)
                sign = False
                literal = variable

            literal_list.append(Literal(variable=variable, sign=sign, literal=literal))
        clause_list.append(Clause(literal_list=literal_list))
    return Cnf(clause_list=clause_list, clause_num=clause_num, variable_num=variable_num)


if __name__ == "__main__":
    cnf = cnf_parse("./raw/test.cnf")
    print('cnf', cnf)
