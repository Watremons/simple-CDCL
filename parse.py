from models import Literal, Clause, Cnf


def cnf_parse(file_path: str) -> Cnf:
    """
    Method:
        Parse the .cnf file to a Cnf instance
    Params:
        file_path: the file path of .cnf file
    """
    file_content = []
    with open(file_path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            elif line.startswith('c'):
                # Skip the comment lines which starts with 'c' and delete '\n' at the end
                pass
            elif line.startswith('p'):
                # Get the first line after comment, starts with p cnf
                word_list = line.split(' ')
                assert word_list[
                    1] == "cnf", "InputError: Context need to start with 'p' and 'cnf'"
                variable_num = int(word_list[2])
                clause_num = int(word_list[3])
            else:
                file_content.append(line.rstrip('\n'))
        f.close()

    assert variable_num is not None and clause_num is not None, "InputError: Context need to start with 'p' and 'cnf'"
    assert clause_num == (
        len(file_content)
    ), "InputError: The lines of context <int:{file_content}> is not equal to clause <int:{clause_num}>".format(
        file_content=len(file_content), clause_num=clause_num)
    # Read every line as a clause
    clause_list = []
    for line_index in range(clause_num):
        raw_literal_list = file_content[line_index].split(' ')
        raw_literal_list = raw_literal_list[:-1]
        literal_list = []
        for raw_literal in raw_literal_list:
            if raw_literal.startswith('-'):
                # Handle a negative literal
                variable = int(raw_literal.lstrip('-'))
                sign = False
                literal = variable + variable_num
            else:
                # Handle a positive literal
                variable = int(raw_literal)
                sign = True
                literal = variable
            literal_list.append(
                Literal(variable=variable, sign=sign, literal=literal))
        clause_list.append(Clause(literal_list=literal_list))
    return Cnf(clause_list=clause_list,
               clause_num=clause_num,
               variable_num=variable_num)


if __name__ == "__main__":
    cnf = cnf_parse("./raw/test4.cnf")
    print('cnf', cnf)
    # print(cnf.clause_list[1])
