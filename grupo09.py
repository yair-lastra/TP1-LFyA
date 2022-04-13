def clean(string_operation):
    buf = ""
    # Para reducir complejidad, se quitan los espacios del input y se reemplaza el símbolo de la potencia por '^'.
    for ch in (string_operation.replace('**', '^')).replace(' ', ''):
        if ch.isnumeric():
            buf += ch
        else:
            if buf:
                yield buf
            if ch == '^':
                yield '**'
            else:
                yield ch
            buf = ''
    if buf:
        yield buf


def get_first_operation(input_operation):
    # Lista con los términos y operadores de la operación completa
    lst = list(clean(input_operation))

    min_idx = 0
    max_idx = 0
    # Se reduce la lista hasta encontrar la primera operación a aplicar. El orden es determinado por la regla PEMDAS.
    while "(" in lst:
        depth = 0
        for idx, value in enumerate(lst):
            if value == "(":
                if depth == 0:
                    min_idx = idx + 1
                depth += 1
            elif value == ")":
                if depth == 1:
                    max_idx = idx
                    break
                else:
                    depth -= 1
        lst = lst[:max_idx][min_idx:]

    # Si en la lista hay más de 2 términos, se determina el operador y los términos de la primera operacion a aplicar
    if sum(map(lambda x: x.isnumeric(), lst)) > 2:
        aux = ""
        for op in [o for o in lst if not o.isnumeric()]:
            if (op == "**") \
                    or ((op == "*" or op == "/") and aux not in ["**", "*", "/"]) \
                    or ((op == "+" or op == "-") and aux == ""):
                aux = op
        for idx, value in enumerate(lst):
            if value == aux:
                min_idx = idx - 1
                max_idx = idx
                break
        while not lst[max_idx].isnumeric():
            max_idx += 1
        lst = lst[:max_idx + 1][min_idx:]
    return "".join(lst)


def calculator(input_operation):
    return float(eval(input_operation)), get_first_operation(input_operation)
