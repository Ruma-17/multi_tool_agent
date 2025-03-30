import os
import requests
from bs4 import BeautifulSoup
import math
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def calculator_tool(expression: str) -> str:
    """
    Calculator tool to evaluate mathematical expressions safely.
    Args:
        expression (str): The mathematical expression to evaluate.
    Returns:
        str: The result of the evaluation or an error message.
    """
    print(f"Received expression: {expression}")
    try:
        # Basic validation and safe evaluation
        allowed_operators = {'+', '-', '*', '/', '(', ')', '.', 'sqrt'}
        # Strip the expression to only include allowed characters
        expression = ''.join([char for char in expression if char in allowed_operators or char.isdigit()])
        
        # Evaluate the expression safely using math library functions
        result = eval(expression, {"__builtins__": None}, {"sqrt": math.sqrt})
        print(f"Calculated result: {result}")
        return f"Calculation result: {result}"
    except Exception as e:
        print(f"Error in calculator: {e}")
        return f"Error in calculator: {e}"

import time
import requests

def search_tool(query: str) -> str:
    """
    Search tool to perform web searches using DuckDuckGo Instant Answer API.
    Args:
        query (str): The search query.
    Returns:
        str: A formatted string containing the search results.
    """
    # Define the DuckDuckGo API URL
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    
    # Retry logic to handle temporary issues (status code 202)
    for attempt in range(3):  # Retry 3 times
        response = requests.get(url)
        print(f"Attempt {attempt + 1}: Status Code {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "Answer" in data and data["Answer"]:
                return f"Answer: {data['Answer']}"
            if "RelatedTopics" in data and data["RelatedTopics"]:
                results = []
                for item in data["RelatedTopics"]:
                    if "Text" in item:
                        title = item["Text"]
                        link = item["FirstURL"]
                        results.append(f"Title: {title}\nLink: {link}\n")
                return "\n".join(results) if results else "No search results found."
            else:
                return "No search results found."
        elif response.status_code == 202:
            print("Received status code 202. Retrying...")
            time.sleep(2)  # Wait for 2 seconds before retrying
        else:
            return f"Error in search: Received status code {response.status_code}"
    
    # If all retries fail, return this message
    return "Error: Unable to retrieve data after multiple attempts."

def define_tool(term: str) -> str:
    """
    Definition tool to look up definitions of terms using an online dictionary.
    Args:
        term (str): The term to define.
    Returns:
        str: The definition of the term or an error message.
    """
    print(f"Looking up definition for: {term}")
    url = f"https://www.dictionary.com/browse/{term}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        definition = soup.find("span", {"class": "one-click-content"})
        if definition:
            print(f"Found definition: {definition.get_text()}")
            return f"Definition of {term}: {definition.get_text()}"
        else:
            return f"Definition of {term} not found."
    else:
        return f"Error in definition lookup: Received status code {response.status_code}"

def query_llm(prompt: str) -> str:
    """
    Query the LLM to determine which tool to use based on the prompt.
    Args:
        prompt (str): The user's query.
    Returns:
        str: The tool name to invoke.
    """
    # System message to give context about the available tools
    system_message = {
        "role": "system",
        "content": (
            "You are an intelligent assistant capable of performing the following tasks:\n"
            "- `calculator_tool`: Evaluate simple mathematical expressions like '2+2'.\n"
            "- `search_tool`: Perform web searches for information based on a query.\n"
            "- `define_tool`: Provide definitions for terms or concepts.\n"
            "Based on the user's query, select the correct tool to use and provide the relevant output."
        )
    }
    
    # Make the API call with the additional system message
    print(f"Querying LLM with prompt: {prompt}")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[system_message, {"role": "user", "content": prompt}]
    )
    
    # Access the content of the model's response
    tool_name = response.choices[0].message.content.strip().lower()
    print(f"LLM response: {tool_name}")

    # Map the LLM response to the correct tool based on keywords
    if 'calculator' in tool_name:
        return 'calculator_tool'
    elif 'search' in tool_name:
        return 'search_tool'
    elif 'define' in tool_name:
        return 'define_tool'
    else:
        return 'No valid tool identified.'

def invoke_tools(query: str) -> str:
    """
    Invoke the correct tool based on the query.
    Args:
        query (str): The user's query.
    Returns:
        str: The result of the tool invocation.
    """
    tool_name = query_llm(query)
    print(f"Tool identified: {tool_name}")
    
    # Map tool name to the actual function
    if tool_name == 'calculator_tool':
        return calculator_tool(query)
    elif tool_name == 'search_tool':
        return search_tool(query)
    elif tool_name == 'define_tool':
        return define_tool(query)
    else:
        return "No valid tool identified."

def main():
    """
    Main function to interact with the user.
    """
    while True:
        query = input("Please enter your query (or 'exit' to quit): ").strip()
        
        if query.lower() == "exit":
            print("Exiting...")
            break
        
        # Invoke the tool and print the result
        result = invoke_tools(query)
        print(f"Result: {result}")

# Start the main interaction loop
if __name__ == "__main__":
    main()
