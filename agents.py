import langgraph
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage, HumanMessage

# Define tools
@tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

# Create a function to handle tool execution
def tool_execution(state: dict):
    tool_name = state["tool_name"]
    tool_args = state["tool_args"]
    
    tools = {"add_numbers": add_numbers, "multiply_numbers": multiply_numbers}
    
    if tool_name in tools:
        result = tools[tool_name](**tool_args)
        return {"response": ToolMessage(name=tool_name, content=str(result))}
    else:
        return {"response": "Tool not found"}

# Build LangGraph workflow
graph = langgraph.Graph()
graph.add_node("tool_execution", tool_execution)
graph.set_entry_point("tool_execution")

graph_compiled = graph.compile()

# Example input
state = {"tool_name": "add_numbers", "tool_args": {"a": 5, "b": 3}}
response = graph_compiled.invoke(state)
print(response)
