from client import MCTSEngine

def main():
    def transition(s, a):
        return s + a
    def reward_fn(s):
        return 1.0 if s >= 2 else 0.0

    mcts = MCTSEngine(actions=[1, -1], get_next_state_fn=transition, eval_rollout_fn=reward_fn)
    res = mcts.search(0, iterations=150)
    print("MCTS Search Engine Verification:")
    print(f"Best Action: {res['best_action']}")
    print(f"Branch Statistics: {res['children_stats']}")

if __name__ == "__main__":
    main()
