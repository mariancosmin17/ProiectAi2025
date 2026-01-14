from typing import List, Tuple
from .models import TreeNode


def alphabeta_minimax(root: TreeNode) -> Tuple[int, int, List[str]]:
    """
    Returnează:
      (root_value, visited_leaves, trace)
    visited_leaves = câte frunze au fost evaluate efectiv (cu alpha-beta pruning).
    """

    visited_leaves = 0
    trace: List[str] = []

    def is_leaf(node: TreeNode) -> bool:
        return node.value is not None

    def rec(node: TreeNode, alpha: int, beta: int, depth: int) -> int:
        nonlocal visited_leaves, trace

        indent = "  " * depth

        if is_leaf(node):
            visited_leaves += 1
            trace.append(f"{indent}Leaf -> {node.value}")
            return node.value

        if not node.children or not node.type:
            # fallback safety
            trace.append(f"{indent}Nod invalid (fără copii/type).")
            return 0

        if node.type == "MAX":
            v = -10**9
            trace.append(f"{indent}MAX node (α={alpha}, β={beta})")
            for idx, child in enumerate(node.children):
                child_val = rec(child, alpha, beta, depth + 1)
                v = max(v, child_val)
                alpha = max(alpha, v)
                trace.append(f"{indent}  -> after child {idx+1}: v={v}, α={alpha}, β={beta}")
                if beta <= alpha:
                    trace.append(f"{indent}  PRUNE (β<=α) la MAX după copilul {idx+1}")
                    break
            return v

        # MIN
        v = 10**9
        trace.append(f"{indent}MIN node (α={alpha}, β={beta})")
        for idx, child in enumerate(node.children):
            child_val = rec(child, alpha, beta, depth + 1)
            v = min(v, child_val)
            beta = min(beta, v)
            trace.append(f"{indent}  -> after child {idx+1}: v={v}, α={alpha}, β={beta}")
            if beta <= alpha:
                trace.append(f"{indent}  PRUNE (β<=α) la MIN după copilul {idx+1}")
                break
        return v

    root_value = rec(root, -10**9, 10**9, 0)
    return root_value, visited_leaves, trace
