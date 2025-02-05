import re
from tabulate import tabulate
import itertools

# Liste des portes logiques
logic_gates = ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"]
logical_operations = []

def apply_gate(gate, a, b):
    if gate == "AND":
        return a & b
    elif gate == "OR":
        return a | b
    elif gate == "NAND":
        return int(not (a & b))
    elif gate == "NOR":
        return int(not (a | b))
    elif gate == "XOR":
        return a ^ b
    elif gate == "XNOR":
        return int(not (a ^ b))
    return 0

def get_unique_pre_values(logical_operations):
    all_before_equal = set()
    all_after_equal = set()

    for operation in logical_operations:
        all_before_equal.add(operation["e1"])
        all_before_equal.add(operation["s2"])
        all_after_equal.add(operation["e2"])

    return list(all_before_equal - all_after_equal)

def generate_truth_table(logical_operations):
    unique_values = get_unique_pre_values(logical_operations)
    unique_values.sort(reverse=True)  # Trier pour l'affichage
    combinations = list(itertools.product([0, 1], repeat=len(unique_values)))

    headers = unique_values + [op["e2"] for op in logical_operations]
    tableau = []

    for combo in combinations:
        inputs = dict(zip(unique_values, combo))
        results = []

        for op in logical_operations:
            e1_val = inputs.get(op["e1"])
            s2_val = inputs.get(op["s2"])

            if e1_val is None or s2_val is None:
                raise ValueError(f"Impossible de trouver {op['e1']} ou {op['s2']}.")

            result = apply_gate(op["gate"], e1_val, s2_val)
            results.append(result)
            inputs[op["e2"]] = result

        tableau.append(list(combo) + results)

    return tabulate(tableau, headers=headers, tablefmt="grid")


def find_logic_gates(text):
    for logic_gate in logic_gates:
        if logic_gate in text:
            return logic_gate
    return None


def parse_expression(expression):
    pattern = r"^(\w+)\s(AND|OR|NAND|NOR|XOR|XNOR)\s(\w+)\s=\s(\w+)$"

    match = re.match(pattern, expression)
    if match:
        e1 = match.group(1)
        gate = match.group(2)
        s2 = match.group(3)
        e2 = match.group(4)

        result = {
            "e1": e1,
            "gate": gate,
            "s2": s2,
            "e2": e2
        }
        return result

    else:
        return "Invalid format."



i = 0
print('Porte logique : AND, OR, NOT, NAND, NOR, XOR, "XNOR')
print("Format des expressions : e1 AND e2 = s1")
print('Entrez "stop" pour terminer.')
while True:
    expression = input("Entez une porte logique :")
    if expression == "stop":
        break
    else:
        parsed_data = parse_expression(expression)
        if "Invalid format." == parsed_data:
            print(parsed_data)
            continue
        logical_operations.append(parsed_data)
        print("Porte logique enregistré.")

print(generate_truth_table(logical_operations))

input("Pressez entré pour terminer :")


"""
Exemple :
x1 AND x2 = y1
y1 XOR x3 = y2
stop
"""