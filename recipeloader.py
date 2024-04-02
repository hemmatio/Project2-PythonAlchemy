from __future__ import annotations
from typing import Any, Optional
import json

def split_text(text: str) -> list[tuple]:
    """splits the combined elements at the /
    for example: 'rain, smoke / rain, smog' becomes [(rain, smoke), (rain, fog)]
    if the text is $DEFAULT return an empty list"""
    if text.lower() == '$default':
        return []
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
    discovered: list[_Vertex]

    def __init__(self, file: json):
        self._vertices = {}
        self.discovered = []
        self.load_vertices(file)

    def load_vertices(self, file: json) -> None:
        """Loads all vertices form the file"""
        data = json.load(file)
        item_created, recipes = '', []
        for row in data:
            for key in row:
                if key == 'NAME':
                    item_created = row[key].lower()
                else:  # key == 'RECIPES'
                    recipes = split_text(row[key].lower())

            if not recipes:
                self.add_vertex(item_created)
                self.discovered.append(self._vertices[item_created])
            for combo in recipes:
                item1, item2 = combo
                self.add_edge(item_created, item1, item2)

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

    def combine(self, item1, item2) -> tuple[bool, Optional[str]]:
        """
        Combine item1 and item2, add the combined item to self.discovered returns whether
        there is a valid combination and the created items name
        """
        discovered_items = {vertex.item for vertex in self.discovered}
        if item1 not in discovered_items or item2 not in discovered_items:
            # print('You may not craft with items you have not yet discovered.')
            return (False, None)
        if item2 not in self._vertices[item1].neighbours:
            # print('This is not a valid crafting recipe.')
            return (False, None)
        else:
            crafted_item = self._vertices[item1].neighbours[item2]
            if crafted_item in self.discovered:
                # print(f"You have already discovered {crafted_item.item}.")
                return (True, crafted_item.item.title())
            self.discovered.append(crafted_item)
            # print(f'You have discovered {crafted_item.item}! Good job')
            return (True, crafted_item.item.title())

    def itemobtained(self, item1, item2) -> str:
        """
        ommited
        :param item1:
        :param item2:
        :return:
        """
        if item2 not in self._vertices[item1].neighbours:
            return "zebi"
        crafted_item = self._vertices[item1].neighbours[item2]
        self.discovered.append(crafted_item)
        return crafted_item.item

    def inventory(self) -> None:
        """
        Print the user's discovered items
        """
        total = len(self._vertices)
        print('INVENTORY:')
        for vertex in self.discovered:
            print('     ' + vertex.item)
        print(f'You have discovered {len(self.discovered)}/{total} items so far.')
