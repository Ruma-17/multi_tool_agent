# main.py
import os
from tools import calculator_tool, search_tool, define_tool, query_llm

def invoke_tools(query: str) -> str:
    """
    Invoke the correct tool based on the user's query.
    Args:
        query (str): The user's query.
    Returns:
        str: The result from the invoked tool.
    """
    llm_prompt = f"User's query: {query}\nWhich tool should be used?"
    tool_name = query_llm(llm_prompt)  # Get the correct tool name based on the query

    if tool_name == 'calculator_tool':
        # Call the calculator tool
        return calculator_tool(query)  # Assuming query is an expression like "2+2"
    elif tool_name == 'search_tool':
        # Call the search tool
        return search_tool(query)  # Assuming query is a search term like "best pizza places in New York"
    elif tool_name == 'define_tool':
        # Call the define tool
        return define_tool(query)  # Assuming query is a term like "Artificial Intelligence"
    else:
        return "No valid tool identified."


def main():
    """
    Main function to handle user input and invoke appropriate tools.
    """
    while True:
        query = input("Please enter your query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        response = invoke_tools(query)
        print(response)

if __name__ == "__main__":
    main()
