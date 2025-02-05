from tabulate import tabulate
import itertools

# Fonction de simulation des portes logiques
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

# Fonction pour extraire les variables d'entrée uniques
def get_unique_pre_values(logical_operations):
    all_before_equal = set()
    all_after_equal = set()

    for operation in logical_operations:
        all_before_equal.add(operation["e1"])
        all_before_equal.add(operation["s2"])
        all_after_equal.add(operation["e2"])

    return list(all_before_equal - all_after_equal)

# Fonction pour générer le tableau des vérités
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

# ============================ TESTS ============================ #

# Test 1 : Simple AND et OR
print("\n🔹 Test 1 : AND et OR")
test1 = [
    {'e1': 'A', 'gate': 'AND', 's2': 'B', 'e2': 'X'},
    {'e1': 'X', 'gate': 'OR', 's2': 'C', 'e2': 'Y'}
]
print(generate_truth_table(test1))

# Test 2 : XOR et NAND
print("\n🔹 Test 2 : XOR et NAND")
test2 = [
    {'e1': 'P', 'gate': 'XOR', 's2': 'Q', 'e2': 'Z1'},
    {'e1': 'Z1', 'gate': 'NAND', 's2': 'R', 'e2': 'Z2'}
]
print(generate_truth_table(test2))

# Test 3 : Chaînage logique plus complexe
print("\n🔹 Test 3 : Chaînage complexe")
test3 = [
    {'e1': 'X1', 'gate': 'AND', 's2': 'X2', 'e2': 'Y1'},
    {'e1': 'Y1', 'gate': 'XOR', 's2': 'X3', 'e2': 'Y2'},
    {'e1': 'Y2', 'gate': 'OR', 's2': 'X4', 'e2': 'Y3'}
]
print(generate_truth_table(test3))

# Test 4 : Toutes les portes logiques utilisées
print("\n🔹 Test 4 : Toutes les portes logiques")
test4 = [
    {'e1': 'A', 'gate': 'AND', 's2': 'B', 'e2': 'X1'},
    {'e1': 'X1', 'gate': 'OR', 's2': 'C', 'e2': 'X2'},
    {'e1': 'X2', 'gate': 'XOR', 's2': 'D', 'e2': 'X3'},
    {'e1': 'X3', 'gate': 'NAND', 's2': 'E', 'e2': 'X4'},
    {'e1': 'X4', 'gate': 'NOR', 's2': 'F', 'e2': 'X5'},
    {'e1': 'X5', 'gate': 'XNOR', 's2': 'G', 'e2': 'Y'}
]
print(generate_truth_table(test4))

# Test 5 : Utilisation de sorties comme entrees
print("\n🔹 Test 5 : Sorties réutilisées comme entrees")
test5 = [
    {'e1': 'I1', 'gate': 'AND', 's2': 'I2', 'e2': 'S1'},
    {'e1': 'S1', 'gate': 'XOR', 's2': 'I3', 'e2': 'S2'},
    {'e1': 'S2', 'gate': 'NOR', 's2': 'I4', 'e2': 'S3'},
    {'e1': 'S3', 'gate': 'OR', 's2': 'I5', 'e2': 'OUT'}
]
print(generate_truth_table(test5))
