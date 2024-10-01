from typing import Dict, Any, Callable, List
from typing import Optional

class Tool:
    def __init__(self, name: str, func: Callable, description: str, parameters: Dict[str, Any]):
        self.name = name
        self.func = func
        self.description = description
        self.parameters = parameters

class ToolRegistry:
    _instance = None
    _tools: Dict[str, Tool] = {}

    @classmethod
    def register(cls, *tools: tuple[Tool]):
        for tool in tools:
            print(f"Registering tool: {tool.name}")  # Debug statement
            cls._tools[tool.name] = tool

    @classmethod
    def get_tool(cls, name: str) -> Tool:
        return cls._tools.get(name)

    @classmethod
    def get_all_tools(cls) -> Dict[str, Tool]:
        return cls._tools

    @classmethod
    def get_tool_description(cls, name: str) -> Optional[Dict[str, Any]]:
        tool = cls.get_tool(name)
        if tool is None:
            return None  # or return {} if you prefer an empty dictionary

        # Create a copy of the tool parameters and remove 'required' from properties
        properties = {
            param: {k: v for k, v in details.items() if k != "required"}
            for param, details in tool.parameters.items()
        }

        # Ensure the 'required' field is always a list
        required_params = [param for param, details in tool.parameters.items() if details.get("required", False)]

        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required_params if required_params else []  # Ensure it's always an array
                }
            }
        }

   


