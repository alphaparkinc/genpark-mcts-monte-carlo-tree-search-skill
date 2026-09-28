import sys
import json
from client import MCTSEngine

mcts = MCTSEngine(actions=["explore_left", "explore_right", "advance_forward"])

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-mcts-monte-carlo-tree-search-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "mcts_plan",
                    "description": "Perform Monte Carlo Tree Search sequential planning for decision-making",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "root_state": {"type": "string", "default": "init"},
                            "iterations": {"type": "integer", "default": 100}
                        }
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "mcts_plan":
            st = args.get("root_state", "init")
            it = args.get("iterations", 100)
            data = mcts.search(st, iterations=it)
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
