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

    def __init__(self, file: json):
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

    def combine(self, item1, item2) -> tuple[bool, Optional[str]]:
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

    def inventory(self) -> None:
        """
        Prints a list of all the items that have been discovered so far, along with a
        count of discovered items versus total items.
        """
        total = len(self._vertices)
        print('INVENTORY:')
        for vertex in self.discovered:
            print('     ' + vertex.item)
        print(f'You have discovered {len(self.discovered)}/{total} items so far.')
