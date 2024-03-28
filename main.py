# """
# Python Alchemy for CSC111 by YC, BG, OH, NN
# class _Vertex and class Graph originally sourced from CSC111 prep starter code.
# """
#
# from __future__ import annotations
# from typing import Any
#
#
# class _Vertex:
#     """A vertex in a graph.
#
#     Instance Attributes:
#         - item: The data stored in this vertex.
#         - neighbours: The vertices that are adjacent to this vertex.
#
#     Representation Invariants:
#         - self not in self.neighbours
#         - all(self in u.neighbours for u in self.neighbours)
#     """
#     item: Any
#     neighbours: set[_Vertex]
#
#     def __init__(self, item: Any, neighbours: set[_Vertex]) -> None:
#         """Initialize a new vertex with the given item and neighbours."""
#         self.item = item
#         self.neighbours = neighbours
#
#     def degree(self) -> int:
#         """Return the degree of this vertex."""
#         return len(self.neighbours)
#
#     def check_connected(self, target_item: Any, visited: set[_Vertex]) -> bool:
#         """Return whether this vertex is connected to a vertex corresponding to the target_item,
#         WITHOUT using any of the vertices in visited.
#
#         Preconditions:
#             - self not in visited
#         """
#         if self.item == target_item:
#             # Our base case: the target_item is the current vertex
#             return True
#         else:
#             visited.add(self)  # Add self to the set of visited vertices
#             for u in self.neighbours:
#                 if u not in visited:  # Only recurse on vertices that haven't been visited
#                     if u.check_connected(target_item, visited):
#                         return True
#
#             return False
#
#
# class Graph:
#     """A graph.
#
#     Representation Invariants:
#         - all(item == self._vertices[item].item for item in self._vertices)
#     """
#     # Private Instance Attributes:
#     #     - _vertices:
#     #         A collection of the vertices contained in this graph.
#     #         Maps item to _Vertex object.
#     _vertices: dict[Any, _Vertex]
#
#     def __init__(self) -> None:
#         """Initialize an empty graph (no vertices or edges)."""
#         self._vertices = {}
#
#     def add_vertex(self, item: Any) -> None:
#         """Add a vertex with the given item to this graph.
#
#         The new vertex is not adjacent to any other vertices.
#
#         Preconditions:
#             - item not in self._vertices
#         """
#         if item not in self._vertices:
#             self._vertices[item] = _Vertex(item, set())
#
#     def add_edge(self, item1: Any, item2: Any) -> None:
#         """Add an edge between the two vertices with the given items in this graph.
#
#         Raise a ValueError if item1 or item2 do not appear as vertices in this graph.
#
#         Preconditions:
#             - item1 != item2
#         """
#         if item1 in self._vertices and item2 in self._vertices:
#             v1 = self._vertices[item1]
#             v2 = self._vertices[item2]
#
#             # Add the new edge
#             v1.neighbours.add(v2)
#             v2.neighbours.add(v1)
#         else:
#             # We didn't find an existing vertex for both items.
#             raise ValueError
#
#     def adjacent(self, item1: Any, item2: Any) -> bool:
#         """Return whether item1 and item2 are adjacent vertices in this graph.
#
#         Return False if item1 or item2 do not appear as vertices in this graph.
#         """
#         if item1 in self._vertices and item2 in self._vertices:
#             v1 = self._vertices[item1]
#             return any(v2.item == item2 for v2 in v1.neighbours)
#         else:
#             # We didn't find an existing vertex for both items.
#             return False
#
#     def connected(self, item1: Any, item2: Any) -> bool:
#         """Return whether item1 and item2 are connected vertices in this graph.
#
#         Return False if item1 or item2 do not appear as vertices in this graph.
#
#         >>> g = Graph()
#         >>> g.add_vertex(1)
#         >>> g.add_vertex(2)
#         >>> g.add_vertex(3)
#         >>> g.add_vertex(4)
#         >>> g.add_edge(1, 2)
#         >>> g.add_edge(2, 3)
#         >>> g.connected(1, 3)
#         True
#         >>> g.connected(1, 4)
#         False
#         """
#         if item1 in self._vertices and item2 in self._vertices:
#             v1 = self._vertices[item1]
#             return v1.check_connected(item2, set())  # Pass in an empty "visited" set
#         else:
#             return False
#
#     def get_neighbours(self, item: Any) -> set:
#         """Return a set of the neighbours of the given item.
#
#         Note that the *items* are returned, not the _Vertex objects themselves.
#
#         Raise a ValueError if item does not appear as a vertex in this graph.
#         """
#         if item in self._vertices:
#             v = self._vertices[item]
#             return {neighbour.item for neighbour in v.neighbours}
#         else:
#             raise ValueError
#
#     def get_all_vertices(self, kind: str = '') -> set:
#         """Return a set of all vertex items in this graph.
#
#         If kind != '', only return the items of the given vertex kind.
#
#         Preconditions:
#             - kind in {'', 'user', 'book'}
#         """
#         if kind != '':
#             return {v.item for v in self._vertices.values() if v.kind == kind}
#         else:
#             return set(self._vertices.keys())
#
#     def get_vertices(self) -> dict[Any, _Vertex]:
#         """Return all the vertices in this graph. (As opposed to a set of their items)"""
#         return self._vertices
