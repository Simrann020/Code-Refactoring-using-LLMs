import ast

class ASTParser:
    def __init__(self, code):
        self.tree = ast.parse(code)

    def extract_functions(self):
        """Extract function names from the code."""
        return [node.name for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef)]

    def extract_variables(self):
        """Extract variable names from the code."""
        return list(set(node.id for node in ast.walk(self.tree) if isinstance(node, ast.Name)))

    def extract_operations(self):
        """Extract arithmetic operations from the code."""
        operations = {
            ast.Add: "Addition",
            ast.Sub: "Subtraction",
            ast.Mult: "Multiplication",
            ast.Div: "Division",
            ast.Mod: "Modulus"
        }
        return [operations[type(node)] for node in ast.walk(self.tree) if type(node) in operations]

# Example Usage
if __name__ == "__main__":
    sample_code = """
def add(a, b):
    result = a + b
    return result

x = 10
y = 20
z = x * y
"""

    parser = ASTParser(sample_code)

    print("Functions:", parser.extract_functions())
    print("Variables:", parser.extract_variables())
    print("Operations:", parser.extract_operations())
