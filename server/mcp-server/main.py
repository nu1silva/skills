import uvicorn
from fastapi import FastAPI, Request
from mcp.server import Server
from mcp.server.sse import SseServerTransport
import mcp.types as types
from gherkin.parser import Parser
from gherkin.errors import ParserError

# 1. Initialize FastAPI app and MCP Server
app = FastAPI(title="Gherkin MCP Server")
server = Server("gherkin-quality-checker")

# 2. Define the MCP transport layer for FastAPI (SSE)
sse = SseServerTransport("/messages")

# 3. Define the Tool Registration
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="analyze_gherkin",
            description="Analyzes Gherkin content for syntax errors and quality best practices.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The Gherkin feature file content"
                    }
                },
                "required": ["content"]
            }
        )
    ]

# 4. Define the Tool Logic
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name != "analyze_gherkin":
        raise ValueError(f"Unknown tool: {name}")

    content = arguments.get("content", "")
    parser = Parser()
    issues = []

    try:
        gherkin_document = parser.parse(content)
        feature = gherkin_document.get('feature', {})

        for child in feature.get('children', []):
            scenario = child.get('scenario')
            if scenario:
                step_count = len(scenario.get('steps', []))
                
                if step_count > 10:
                    issues.append(f"Warning: Scenario '{scenario['name']}' is too long ({step_count} steps).")
                
                if step_count == 0:
                    issues.append(f"Error: Scenario '{scenario['name']}' has no steps.")

        if not issues:
            result_text = "✅ Gherkin is valid and follows best practices."
        else:
            result_text = "⚠️ Quality Issues Found:\n" + "\n".join(f"- {i}" for i in issues)

    except ParserError as e:
        result_text = f"❌ Syntax Error: {str(e)}"
    except Exception as e:
        result_text = f"❌ Unexpected Error: {str(e)}"

    return [types.TextContent(type="text", text=result_text)]

# 5. FastAPI Routes for MCP Communication
@app.get("/sse")
async def sse_endpoint(request: Request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await server.run(
            streams[0], streams[1], server.create_initialization_options()
        )

@app.post("/messages")
async def messages_endpoint(request: Request):
    await sse.handle_post_message(request.scope, request.receive, request._send)

# 6. Run the local server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)