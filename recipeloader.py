"""
File Outline
===============================
This file defines a simple graph-based system for tracking combinations of elements to
create new elements. The system allows for loading elements and their combinations
from a file, adding new elements, combining known elements to discover new ones, and
tracking the inventory of discovered elements.

Copyright and Usage Information
===============================
This file is provided solely for the private use of the teaching staff
of CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2024 Omid Hemmati, Yianni Culmone, Neyl Nasr, Benjamin Gavriely
"""

from __future__ import annotations
from typing import Optional
import json


def split_text(text: str) -> list[tuple]:
    """
    Splits the combined elements at the "/" and returns a list of tuples representing combinations.
    If the input text is "$DEFAULT", returns an empty list.

    Preconditions:
    - text must be a non-empty string.

    :param text: A string containing combinations separated by "/".
    :return: A list of tuples, each containing a pair of elements.
    """
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
    A class representing a vertex in a graph, used to model an element.

    Instance Attributes:
    - item: The name of the element.
    - neighbours: A dictionary mapping combinations to the resulting element.

    Representation Invariants:
    - item must be a non-empty string.
    - neighbours must be a dictionary with string keys and _Vertex values.
    """

    item: str
    neighbours: dict[str, _Vertex]

    def __init__(self, item: str) -> None:
        """
        Initialize a new vertex with the given item. Neighbours are initialized as empty.

        :param item: The name of the element.
        """
        self.item = item
        self.neighbours = {}


class Graph:
    """
    A graph class representing the relationships between elements through vertices and edges.

    Instance Attributes:
    - _vertices: A dictionary mapping element names to _Vertex instances.
    - discovered: A list of _Vertex instances that have been discovered.

    Representation Invariants:
    - _vertices must be a dictionary with string keys and _Vertex values.
    - discovered must be a list of _Vertex instances, and each instance must also exist in _vertices.
    """
    _vertices: dict[str, _Vertex]
    discovered: list[_Vertex]

    def __init__(self, file: json) -> None:
        """
        A graph class representing the relationships between elements through vertices and edges.

        Instance Attributes:
        - _vertices: A dictionary mapping element names to _Vertex instances.
        - discovered: A list of _Vertex instances that have been discovered.

        Representation Invariants:
        - _vertices must be a dictionary with string keys and _Vertex values.
        - discovered must be a list of _Vertex instances, and each instance must also exist in _vertices.
        """
        self._vertices = {}
        self.discovered = []
        self.load_vertices(file)

    def update(self, items: list[str]) -> None:
        """
        Updates the discovered vertices in self to be in accordance to items. The original discovered vertices
        will always be a subset of the updated discovered vertices.
        Preconditions:
        - all the items are the items of existing vertices in self
        :param items: The list of items that is used to update self.discovered
        """
        vertices = []
        # if all the items in discovered are not in items, then it doesn't mutate
        for item in items:
            if item not in self._vertices:
                raise ValueError
            vertices.append(self._vertices[item])
        if all(vertex.item in items for vertex in self.discovered):
            self.discovered = vertices

    def downdate(self) -> list[str]:
        """
        Return a list of the items given by the currently discovered vertices
        Preconditions:
        - all the items in self.discovered are in self._vertices
        :return: a list of the items in self.discovered
        """
        items = []
        for vertex in self.discovered:
            if vertex not in self._vertices.values():
                raise ValueError
            else:
                items.append(vertex.item)
        return items

    def get_vertices(self) -> dict[str, _Vertex]:
        """
        Gets the vertices of the graph
        :return: the vertices of the graph
        """
        return self._vertices

    def load_vertices(self, file: json) -> None:
        """
        Loads all vertices from the file and updates the graph structure accordingly.

        Preconditions:
        - file must be a valid JSON file in the specified format for elements and recipes.
        Example format can be found in recipes.json

        :param file: A JSON file to load vertices from.
        """
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
        """
        Add a vertex with the given item name to the graph if it doesn't already exist.

        Preconditions:
        - item must be a non-empty string.

        :param item: The name of the element to add as a vertex.
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item)

    def add_edge(self, item_created: str, item1: str, item2: str) -> None:
        """
        Add an edge between two vertices, representing a combination that creates a new element.

        Preconditions:
        - item_created, item1, and item2 must be non-empty strings.
        - The combination (item1, item2) must be valid and not already exist in the graph.

        :param item_created: The name of the element created by combining item1 and item2.
        :param item1: The name of the first element in the combination.
        :param item2: The name of the second element in the combination.
        """
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

    def combine(self, item1: str, item2: str) -> tuple[bool, Optional[str]]:
        """
        Attempts to combine two items and discover a new item. Updates the discovered list
        if the combination is successful.

        Preconditions:
        - item1 and item2 must be strings corresponding to items already discovered.

        :param item1: The name of the first item to combine.
        :param item2: The name of the second item to combine.
        :return: A tuple containing a boolean indicating success, and optionally the name of the discovered item.
        """
        discovered_items = {vertex.item for vertex in self.discovered}
        if item1 not in discovered_items or item2 not in discovered_items:
            # print('You may not craft with items you have not yet discovered.')
            return False, None
        if item2 not in self._vertices[item1].neighbours:
            # print('This is not a valid crafting recipe.')
            return False, None
        else:
            crafted_item = self._vertices[item1].neighbours[item2]
            if crafted_item in self.discovered:
                # print(f"You have already discovered {crafted_item.item}.")
                return True, crafted_item.item.title()
            self.discovered.append(crafted_item)
            # print(f'You have discovered {crafted_item.item}! Good job')
            return True, crafted_item.item.title()

    def possible_new_combo(self, item1: str, item2: str) -> bool:
        """
        This method returns wheither you can create a new element with element 1 and element 2:
        """
        if (item1 not in self._vertices) or (item2 not in self._vertices):
            return False
        elif item1 in self._vertices[item2].neighbours:
            return False
        return True

    def new_combo(self, item1: str, item2: str, item3: str) -> None:
        """
        This method adds a new combination of two elements if both elements already exist and their combination does not
        """
        if self.possible_new_combo(item1, item2):
            self.add_edge(item3, item1, item2)


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['sys', 'pygame', 'recipeloader', 'random', 'button', 'json'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'no-member': False
    })
