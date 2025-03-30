# Multi-Tool Reasoning Agent

This is a simple LLM-powered agent that uses the ReAct (Reasoning + Acting) pattern to dynamically decide which tools to use when answering a question.

## Features

- ReAct-style reasoning loop using an LLM
- Tool selection: `calculator`, `search`, `define`
- Tool execution and observation handling
- Modular tool design
- Easy to extend with new tools

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/multi_tool_agent.git
cd multi_tool_agent
```

### 2. Set up environment
```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install openai
```

### 3. Add your OpenAI API Key
Set it as an environment variable:
```bash
export OPENAI_API_KEY=your-api-key  # on Linux/Mac
set OPENAI_API_KEY=your-api-key     # on Windows CMD
```

### 4. Run the agent
```bash
python main.py
```

## File Structure

```
multi_tool_agent/
├── tools.py        # Contains calculator, search, and define tools
├── main.py         # Core logic for the ReAct agent
├── README.md       # This file
```

## License

MIT License
