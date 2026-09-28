"""Monte Carlo Tree Search (MCTS / UCT) Engine
100% Python Standard Library (math).
"""

import math

class MCTSNode:
    """MCTS Search Tree Node."""
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.value = 0.0

    def is_fully_expanded(self, all_actions):
        return len(self.children) == len(all_actions)

    def best_child(self, c_param=1.414):
        best = None
        best_uct = -1e9
        for c in self.children:
            if c.visits == 0:
                return c
            uct = (c.value / c.visits) + c_param * math.sqrt(2.0 * math.log(self.visits) / c.visits)
            if uct > best_uct:
                best_uct = uct
                best = c
        return best

class MCTSEngine:
    """Upper Confidence Bounds for Trees search orchestrator."""
    def __init__(self, actions, get_next_state_fn=None, eval_rollout_fn=None):
        self.actions = actions
        self.get_next_state = get_next_state_fn or (lambda s, a: f"{s}::{a}")
        self.eval_rollout = eval_rollout_fn or (lambda s: 1.0)

    def search(self, root_state, iterations=100):
        root = MCTSNode(root_state)
        for _ in range(iterations):
            node = root
            while node.is_fully_expanded(self.actions) and node.children:
                node = node.best_child()

            tried = [c.action for c in node.children]
            untried = [a for a in self.actions if a not in tried]
            if untried:
                action = untried[0]
                next_st = self.get_next_state(node.state, action)
                child = MCTSNode(next_st, parent=node, action=action)
                node.children.append(child)
                node = child

            reward = self.eval_rollout(node.state)

            while node is not None:
                node.visits += 1
                node.value += reward
                node = node.parent

        best_act = max(root.children, key=lambda c: c.visits).action if root.children else self.actions[0]
        return {
            "best_action": best_act,
            "root_visits": root.visits,
            "children_stats": [{"action": c.action, "visits": c.visits, "win_rate": round(c.value / max(1, c.visits), 3)} for c in root.children]
        }
