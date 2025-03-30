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
    try:
        # Use math library functions for safety
        result = eval(expression, {"__builtins__": None}, {"sqrt": math.sqrt})
        return f"Calculation result: {result}"
    except Exception as e:
        return f"Error in calculator: {e}"

def search_tool(query: str) -> str:
    """
    Search tool to perform web searches using the requests and BeautifulSoup libraries.
    Args:
        query (str): The search query.
    Returns:
        str: A formatted string containing the search results.
    """
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = []
        for item in soup.find_all("h3"):
            title = item.get_text()
            link = item.find_parent("a")["href"]
            search_results.append(f"Title: {title}\nLink: {link}\n")
        return "\n".join(search_results) if search_results else "No search results found."
    else:
        return f"Error in search: Received status code {response.status_code}"

def define_tool(term: str) -> str:
    """
    Definition tool to look up definitions of terms using an online dictionary.
    Args:
        term (str): The term to define.
    Returns:
        str: The definition of the term or an error message.
    """
    url = f"https://www.dictionary.com/browse/{term}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        definition = soup.find("span", {"class": "one-click-content"})
        if definition:
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
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Correct way to access the message content from response object
    tool_name = response.choices[0].message['content'].strip().lower()

    # Map the LLM response to the correct tool based on keywords
    if 'calculator' in tool_name:
        return 'calculator_tool'
    elif 'search' in tool_name:
        return 'search_tool'
    elif 'define' in tool_name:
        return 'define_tool'
    else:
        return 'No valid tool identified.'