import re

# Simulating a simple "fake" agent environment
class SearchTool:
    def search(self, query: str):
        # Simulate a search query
        print(f"Agent: SearchTool - Searching for: {query}")
        # Fake results for search
        if query.lower() == "facts about python":
            return "Interesting facts about Python:\n1. Python is named after Monty Python.\n2. Python supports multiple programming paradigms."
        return "No relevant results found."

class DefineTool:
    def define(self, term: str):
        print(f"Agent: DefineTool - Looking up definition for: {term}")
        # Fake definition for Python
        if term.lower() == "python":
            return "Python is a high-level programming language known for its simplicity and readability."
        return f"Definition for {term} not found."

class InvokeTools:
    def invoke(self, query: str):
        print(f"Agent: InvokeTools - Received query: {query}")

        # Step 1: Clean and split the query into parts using regex
        results = []

        # Define regex patterns for "What is" and "facts about" queries
        definition_pattern = re.compile(r"what is (\w+)", re.IGNORECASE)
        facts_pattern = re.compile(r"tell me some interesting facts about (\w+|\w+\s\w+)", re.IGNORECASE)

        # Step 2: Search for the definition part (if it exists)
        definition_match = definition_pattern.search(query)
        if definition_match:
            term = definition_match.group(1).strip()
            print(f"Agent: InvokeTools - Definition part detected: {term}")
            define_tool = DefineTool()
            definition = define_tool.define(term)
            results.append(f"Definition: {definition}")
        else:
            # If no definition part is found, set term to None
            term = None

        # Step 3: Search for the facts part (if it exists)
        if term:
            # If a term was found in the definition part, use it for the facts query
            facts_query = f"facts about {term}"
            print(f"Agent: InvokeTools - Facts part detected: {facts_query}")
            search_tool = SearchTool()
            facts = search_tool.search(facts_query)
            results.append(f"Facts: {facts}")
        else:
            # If no valid term was detected, return no results for facts
            results.append("No valid term for facts found.")

        # If no valid tool is identified, return a message
        if not results:
            results.append("Sorry, I couldn't understand your query. Please try again.")

        # Combine results from all tools
        return "\n".join(results)

# Main function to interact with the user
def main():
    while True:
        query = input("Please enter your query (or 'exit' to quit): ").strip()

        if query.lower() == "exit":
            print("Agent: Main - Exiting...")
            break

        invoke_tools = InvokeTools()
        result = invoke_tools.invoke(query)
        print(f"Final result:\n{result}")
        print(f"Result:\n{result}\n")

# Start the main interaction loop
if __name__ == "__main__":
    main()
