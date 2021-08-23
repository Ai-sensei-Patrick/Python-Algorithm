"""
Quokka Maze
===========

This file represents the quokka maze, a graph of locations where a quokka is
trying to find a new home.

Please help the quokkas find a path from their current home to their
destination such that they have sufficient food along the way!

*** Assignment Notes ***

This is the main file that will be interacted with during testing.
All functions to implement are marked with a `TODO` comment.

Please implement these methods to help the quokkas find their new home!
"""

from typing import List, Union

from vertex import Vertex


class QuokkaMaze:
    """
    Quokka Maze
    -----------

    This class is the undirected graph class that will contain all the
    information about the locations between the Quokka colony's current home
    and their final destination.

    We _will_ be performing some minor adversarial testing this time, so make
    sure you're performing checks and ensuring that the graph is a valid simple
    graph!

    ===== Functions =====

        * block_edge(u, v) - removes the edge between vertex `u` and vertex `v`
        * fix_edge(u, v) - fixes the edge between vertex `u` and `v`. or adds an
            edge if non-existent
        * find_path(s, t, k) - find a SIMPLE path from veretx `s` to vertex `t`
            such that from any location with food along this simple path we
            reach the next location with food in at most `k` steps
        * exists_path_with_extra_food(s, t, k, x) - returns whether it’s
            possible for the quokkas to make it from s to t along a simple path
            where from any location with food we reach the next location with
            food in at most k steps, by placing food at at most x new locations

    ===== Notes ======

    * We _will_ be adversarially testing, so make sure you check your params!
    * The ordering of vertices in the `vertex.edges` does not matter.
    * You MUST check that `k>=0` and `x>=0` for the respective functions
        * find_path (k must be greater than or equal to 0)
        * exists_path_with_extra_food (k and x must be greater than or equal to
            0)
    * This is an undirected graph, so you don't need to worry about the
        direction of traversing during your path finding.
    * This is a SIMPLE GRAPH, your functions should ensure that it stays that
        way.
    * All vertices in the graph SHOULD BE UNIQUE! IT SHOULD NOT BE POSSIBLE
        TO ADD DUPLICATE VERTICES! (i.e the same vertex instance)
    """

    def __init__(self) -> None:
        """
        Initialises an empty graph with a list of empty vertices.
        """
        self.vertices = []
        self.path = None
        self.exist_path = False

    def add_vertex(self, v: Vertex) -> bool:
        """
        Adds a vertex to the graph.
        Returns whether the operation was successful or not.

        :param v - The vertex to add to the graph.
        :return true if the vertex was correctly added, else false
        """
        # TODO implement me, please?
        if v is None:
            return False
        elif v not in self.vertices:
            self.vertices.append(v)
            return True
        return False

    def fix_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Fixes the edge between two vertices, u and v.
        If an edge already exists, then this operation should return False.

        :param u - A vertex
        :param v - Another vertex
        :return true if the edge was successfully fixed, else false.
        """

        # TODO implement me please.
        if v is None or u is None:
            return False
        elif u not in self.vertices or v not in self.vertices:
            return False
        elif v in u.edges and u in v.edges:
            return False
        v.add_edge(u)
        u.add_edge(v)
        return True

    def block_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Blocks the edge between two vertices, u and v.
        Removes the edge if it exists.
        If not, it should be unsuccessful.

        :param u - A vertex
        :param v - Another vertex.
        :return true if the edge was successfully removed, else false.
        """

        # TODO implement me, please!
        if v is None or u is None:
            return False
        elif u not in self.vertices or v not in self.vertices:
            return False
        elif v not in u.edges and u not in v.edges:
            return False
        v.rm_edge(u)
        u.rm_edge(v)
        return True
    
    def find_path_helper(self,s: Vertex,t: Vertex,k: int,ls: List,c: int):
        s.has_visited = True
        
        if s == t:
            self.path = ls.copy()
            s.has_visited = False
            c = c + 1
            return
        
        elif s.has_food:
            c = k
        
        elif c == 0:
            s.has_visited = False
            c = c + 1
            return
        
        for i in s.edges:
            if not i.has_visited: 
                ls.append(i)
                self.find_path_helper(i,t,k,ls,c-1)
                ls.remove(i)
        
        c = c + 1
        s.has_visited = False


    def find_path(
            self,
            s: Vertex,
            t: Vertex,
            k: int
    ) -> Union[List[Vertex], None]:
        """
        find_path returns a SIMPLE path between `s` and `t` such that from any
        location with food along this path we reach the next location with food
        in at most `k` steps

        :param s - The start vertex for the quokka colony
        :param t - The destination for the quokka colony
        :param k - The maximum number of hops between locations with food, so
        that the colony can survive!
        :returns
            * The list of vertices to form the simple path from `s` to `t`
            satisfying the conditions.
            OR
            * None if no simple path exists that can satisfy the conditions, or
            is invalid.

        Example:
        (* means the vertex has food)
                    *       *
            A---B---C---D---E

            1/ find_path(s=A, t=E, k=2) -> returns: [A, B, C, D, E]

            2/ find_path(s=A, t=E, k=1) -> returns: None
            (because there isn't enough food!)

            3/ find_path(s=A, t=C, k=4) -> returns: [A, B, C]

        """

        # TODO implement me please
        if s not in self.vertices or t not in self.vertices or k < 0:
            return
        self.path = None
        ls = [s]
        c = k
        self.find_path_helper(s,t,k,ls,c)
        return self.path

    def exist_path_helper(self,s: Vertex,t: Vertex,k: int,c: int, x: int, f: int):
        s.has_visited = True
        
        if s == t:
            s.has_visited = False
            self.exist_path = True
            c = c + 1
            return 

        elif s.has_food:
            c = k
        
        elif c == 0 and f > 0:
            f = f - 1
            s.added_food = True
            c = k

        elif c == 0 and f == 0:
            s.has_visited = False
            c = c + 1
            return
        
        for i in s.edges:
            if not i.has_visited: 
                self.exist_path_helper(i,t,k,c-1,x,f)
        
        c = c + 1
        s.has_visited = False
        if s.added_food:
            s.added_food = False
            f += 1


    def exists_path_with_extra_food(
        self,
        s: Vertex,
        t: Vertex,
        k: int,
        x: int
    ) -> bool:
        """
        Determines whether it is possible for the quokkas to make it from s to
        t along a SIMPLE path where from any location with food we reach the
        next location with food in at most k steps, by placing food at at most
        x new locations.

        :param s - The start vertex for the quokka colony
        :param t - The destination for the quokka colony
        :param k - The maximum number of hops between locations with food, so
        that the colony can survive!
        :param x - The number of extra foods to add.
        :returns
            * True if with x added food we can complete the simple path
            * False otherwise.

        Example:
        (* means the vertex has food)
                            *
            A---B---C---D---E

            1/ exists_with_extra_food(A, E, 2, 0) -> returns: False
                (because we can't get from A to E with k=2 and 0 extra food)

            2/ exists_with_extra_food(A, E, 2, 1) -> returns: True
                (Yes, if we put food on `C` then we can get to E with k=2)

            3/ exists_with_extra_food(A, E, 1, 6) -> returns: True
                (Yes, if we put food on `B`, `C`, `D` then we reach E!)

        """

        # TODO implement me please
        if s not in self.vertices or t not in self.vertices or x < 0 or k < 0:
            return False
        self.exist_path = False
        c = k
        f = x
        self.exist_path_helper(s,t,k,c,x,f)
        return self.exist_path
