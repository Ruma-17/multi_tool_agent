def calculator(expr: str) -> str:
    try:
        from math import sqrt
        return str(eval(expr, {"__builtins__": None}, {"sqrt": sqrt}))
    except Exception as e:
        return f"Error: {e}"

def search(query: str) -> str:
    print("query is ", str)
    if "countries in africa" in query.lower():
        return "There are 54 countries in Africa."
    return "Search result not found."

def define(term: str) -> str:
    definitions = {
        "entropy": "A measure of randomness or disorder.",
        "neural network": "A machine learning model inspired by the human brain."
    }
    return definitions.get(term.lower(), "Definition not found.")
