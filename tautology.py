''' It's a project of the general knowledge from the GitHubClone\\Python\\boolean_algebra 
except Karnauhg map and Quine mc Cluskey and multiplexer 
'''

'''
^ - AND, -> - IMPLICATION, & - OR, ~ - negetation
'''
import itertools

# Dictionary of operator precedence (higher value means higher precedence)
precedence = {
    '~': 4,  # NOT
    '^': 3,  # AND
    '&': 2,  # OR
    '->': 1  # IMPLICATION (lower precedence)
}

# Define logical operations
def apply_operator(operator, a, b=None):
    if operator == '^':  # AND
        return int(a and b)
    elif operator == '->':  # Implication
        return int(not a or b)
    elif operator == '&':  # OR
        return int(a or b)
    elif operator == '~':  # Negation (only one argument)
        return int(not a)
    else:
        raise ValueError(f"Unsupported operator: {operator}")

# Function to evaluate the expression based on precedence and operators
def evaluate_expression(variables, expression, row_values):
    stack = []
    ops = []

    def process_operator():
        operator = ops.pop()
        print(f"Processing operator: {operator}")
        if operator == '~':  # Unary operator (negation)
            if not stack:
                raise ValueError("Stack is empty, cannot apply unary operator.")
            a = stack.pop()
            print(f"Popped for unary: {a}")
            stack.append(apply_operator(operator, a))
        else:  # Binary operators
            if len(stack) < 2:
                raise ValueError("Stack does not contain enough operands for binary operator.")
            b = stack.pop()
            a = stack.pop()
            print(f"Popped for binary: a={a}, b={b}")
            stack.append(apply_operator(operator, a, b))

    # Replace variables with their corresponding values
    for token in expression:
        #print(f"Token: {token}")
        if token in variables:  # Variable
            stack.append(row_values[variables.index(token)])
            #print(f"Stack after variable {token}: {stack}")
        elif token == '(':  # Open parenthesis
            ops.append(token)
        elif token == ')':  # Close parenthesis, process until matching '('
            while ops and ops[-1] != '(':
                process_operator()
            ops.pop()  # Remove the '('
        elif token in precedence:  # Operator
            while (ops and ops[-1] != '(' and precedence[ops[-1]] >= precedence[token]):
                process_operator()
            ops.append(token)

    # Process remaining operators
    while ops:
        process_operator()

    if len(stack) != 1:
        raise ValueError("Stack should contain exactly one result at the end of evaluation.")

    return stack[0]



# Generate all possible truth values for variables
def generate_truth_table(variables):
    return list(itertools.product([0, 1], repeat=len(variables)))

# Print truth table and check for tautology
def print_truth_table(variables, truth_table, expression):
    results = []
    tautology = True  # To check if the expression is a tautology

    header = "| " + " | ".join(f'{var:^7}' for var in variables) + ' | ' + ' '.join(expression).lower() + ' |'
    print(header)
    print("-" * len(header))

    for row in truth_table:
        output = evaluate_expression(variables, expression, row)

        # Check if it's not a tautology
        if output == 0:
            tautology = False

        results.append(output)
        formatted_row = '| ' + ' | '.join(f"{val:^7}" for val in row) + f" | {output:^7} |"
        print(formatted_row)

    return results, tautology

# Main execution
my_input_string = '( ~ p -> q ^ c ) -> q'  # The logical expression to evaluate
expression = my_input_string.split()  # Split expression into tokens
variables = sorted(set([char for char in expression if char.isalpha()]))  # Extract variables (like p, q, c)

# Generate truth table and evaluate expression
truth_table = generate_truth_table(variables)
results, is_tautology = print_truth_table(variables, truth_table, expression)

print(f'\nThe results of the truth table: {results}')
if is_tautology:
    print("The expression is a tautology.")
else:
    print("The expression is not a tautology.")
