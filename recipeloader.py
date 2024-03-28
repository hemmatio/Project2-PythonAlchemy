import json
from typing import Any


class _Vertex:
    """
    Instance Attributes:
    item: This will be the name of the element
    neighbours: {element_combine: element_created}
    """

    item: str
    neighbours: dict[str, _Vertex]

    def __init__(self, item: str) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = {}



f = open('recipes.json')
data = json.load(f)
f.close()
