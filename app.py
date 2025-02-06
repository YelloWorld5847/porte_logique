from flask import Flask, render_template, request
import re
import itertools

app = Flask(__name__)

logic_gates = ["AND", "OR", "NAND", "NOR", "XOR", "XNOR"]
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
    if not logical_operations:
        return None, None
    unique_values = get_unique_pre_values(logical_operations)
    unique_values.sort(reverse=True)
    combinations = list(itertools.product([0, 1], repeat=len(unique_values)))
    headers = unique_values + [op["e2"] for op in logical_operations]
    tableau = []
    for combo in combinations:
        inputs = dict(zip(unique_values, combo))
        results = []
        for op in logical_operations:
            e1_val = inputs.get(op["e1"], 0)
            s2_val = inputs.get(op["s2"], 0)
            result = apply_gate(op["gate"], e1_val, s2_val)
            results.append(result)
            inputs[op["e2"]] = result
        tableau.append(list(combo) + results)
    return headers, tableau

def parse_expression(expression):
    pattern = r"^(\w+)\s(AND|OR|NAND|NOR|XOR|XNOR)\s(\w+)\s=\s(\w+)$"
    match = re.match(pattern, expression)
    if match:
        return {
            "e1": match.group(1),
            "gate": match.group(2),
            "s2": match.group(3),
            "e2": match.group(4)
        }
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    global logical_operations
    error_message = ""
    if request.method == 'POST':
        expression = request.form.get('expression', '').strip()
        if expression.lower() == "reset":
            logical_operations = []
        else:
            parsed_data = parse_expression(expression)
            if parsed_data:
                logical_operations.append(parsed_data)
            else:
                error_message = "Format invalide. Utiliser: x1 AND x2 = y1"
    headers, tableau = generate_truth_table(logical_operations)
    return render_template('index.html', headers=headers, tableau=tableau, error=error_message)

if __name__ == '__main__':
    app.run(debug=True)