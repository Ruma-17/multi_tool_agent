from tools import calculator, search, define
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import re



tools = {"calculator": calculator, "search": search, "define": define}

PREFIX = """You are an intelligent agent that can reason and use tools.
You have access to the following tools:

calculator(expr: str) — evaluate math expressions
search(query: str) — look up factual info
define(term: str) — give definitions

You will be given a question. Think step by step and use the appropriate tool if needed. Format your responses like:

Thought: ...
Action: <tool>(<input>)
Observation: ...
... (repeat)
Answer: <final answer>

You are not to rerieve any data yourself. If the data has not been provided to you, omit 'Answer' from your response format.

Begin!
"""

def parse_action(output):
    match = re.search(r'Action: (\w+)\((.*)\)', output)
    if match:
        return match.group(1), match.group(2).strip().strip("'").strip('"')
    return None, None

def run_agent(question, llm_fn):
    history = PREFIX + f"\nQuestion: {question}\n"
    while True:
        response = llm_fn(history)
        print(response.strip())
        if "Answer:" in response:
            return response.split("Answer:")[-1].strip()
        tool, arg = parse_action(response)
        if tool in tools:
            observation = tools[tool](arg)
        else:
            observation = f"Unknown tool: {tool}"
        history += f"{response}\nObservation: {observation}\n"

# Example usage
def call_openai(prompt):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{ "role": "user", "content": prompt }])
    return response.choices[0].message.content

if __name__ == "__main__":
    answer = run_agent("What is the total population of India? How does it compare to the USA in percentage?", call_openai)
    print("Final Answer:", answer)
