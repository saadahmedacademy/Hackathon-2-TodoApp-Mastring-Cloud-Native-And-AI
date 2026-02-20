from typing import Callable, Dict, Any, List

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._tool_schemas: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, func: Callable, schema: Dict[str, Any]):
        if name in self._tools:
            raise ValueError(f"Tool '{name}' already registered.")
        self._tools[name] = func
        self._tool_schemas[name] = schema

    def get_tool(self, name: str) -> Callable:
        tool = self._tools.get(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found.")
        return tool

    def get_tool_schema(self, name: str) -> Dict[str, Any]:
        schema = self._tool_schemas.get(name)
        if not schema:
            raise ValueError(f"Schema for tool '{name}' not found.")
        return schema

    def get_all_tool_schemas(self) -> List[Dict[str, Any]]:
        return list(self._tool_schemas.values())