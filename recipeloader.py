from __future__ import annotations
from typing import Any, Optional
import json


def split_text(text: str) -> Optional[list[tuple]]:
    """splits the combined elements at the /
    for example: 'rain, smoke / rain, smog' becomes [(rain, smoke), (rain, fog)]
    if the text is $DEFAULT return None"""
    returnval = []
    split = str.split(text, '/')
    for tup in split:
        tupl = tuple(str.split(tup, ','))
        tupl = tupl[0].strip(), tupl[1].strip()
        returnval.append(tupl)
    return returnval

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


class Graph:
    """
    Instance Atrrributes
    vertices: dict[str, _vertex]
    discovered: set[vertex]
    """
    _vertices: dict[str, _Vertex]
    discovered: set[_Vertex]

    def __init__(self, file: json):
        self._vertices = {}
        self.discovered = set()

    def load_vertices(self, file: json):
        data = json.load(file)
        for row in data:
            for key in row:
                combine = row[key].sp

            self.add_edge()

    def add_vertex(self, item: str) -> None:
        """Add a vertex with the given item to this graph"""
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item)

    def add_edge(self, item_created: str, item1: str, item2: str) -> None:
        """Add an edge between the two vertices with the given items in this graph.
        Add the 2 vertex is they don't exist"""
        if item_created not in self._vertices:
            self.add_vertex(item_created)
        if item1 not in self._vertices:
            self.add_vertex(item1)
        if item2 not in self._vertices:
            self.add_vertex(item2)

        # Add the neighbours
        v0, v1, v2 = self._vertices[item_created], self._vertices[item1], self._vertices[item2]
        v1.neighbours.update({item2: v0})
        v2.neighbours.update({item1: v0})
