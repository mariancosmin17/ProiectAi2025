import random
from typing import Optional
from .models import TreeNode


def generate_tree(
    depth: int = 3,
    branching: int = 2,
    value_min: int = 0,
    value_max: int = 15,
    root_type: str = "MAX",
) -> TreeNode:
    """
    Generează un arbore Minimax:
      - noduri interne: {type: MAX/MIN, children:[...]}
      - frunze: {value:int}
    depth = număr niveluri de decizie (ex: 3 => MAX->MIN->MAX->leaf)
    """
    if depth <= 0:
        return TreeNode(value=random.randint(value_min, value_max))

    node_type = root_type
    next_type = "MIN" if node_type == "MAX" else "MAX"

    children = [
        generate_tree(
            depth=depth - 1,
            branching=branching,
            value_min=value_min,
            value_max=value_max,
            root_type=next_type,
        )
        for _ in range(branching)
    ]
    return TreeNode(type=node_type, children=children)
