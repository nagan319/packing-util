import copy
from enum import Enum
from shapely import Polygon, LineString
from typing import Tuple, List, Union
from custom_types import polyAsList, lineAsList, pointAsTuple
from poly_func import PolyFunc

class LineRelationship(Enum):
    """
    Relationship of two lines depending on the dot product.
    """
    ccw = 0
    cw = 1
    parallel = 2

class Intersection:
    """
    Class to represent an interesction of two edges.

    ### Parameters:
    - edge1: edge stored as list.
    - edge2: edge stored as list.
    - vector1: vector representation of edge1.
    - vector2: vector representation of edge2.
    - edge1_start: Flag indicating if the intersection point is the start of edge1.
    - edge2_start: Flag indicating if the intersection point is the start of edge2.
    - edge1_end: Flag indicating if the intersection point is the end of edge1.
    - edge2_end: Flag indicating if the intersection point is the end of edge2.
    =
    """
    def __init__(self, edge1: lineAsList, edge2: lineAsList, vector1, vector2, edge1_start: bool, edge2_start: bool, edge1_end: bool, edge2_end: bool, pt: pointAsTuple):
        self.edge1 = edge1
        self.edge2 = edge2
        self.vector1 = vector1
        self.vector2 = vector2
        self.edge1_start = edge1_start
        self.edge2_start = edge2_start
        self.edge1_end = edge1_end
        self.edge2_end = edge2_end
        self.pt = pt

class NFP:
    """
    Class that computes NFP between two polygons.

    ### Parameters:
    - poly1: Stationary polygon in list format.
    - poly2: Sliding polygon in list format.
    """

    def __init__(self, poly1: polyAsList, poly2: polyAsList):
        self.stationary = copy.deepcopy(poly1)
        self.sliding = copy.deepcopy(poly2)

        self.starting_point_index = PolyFunc.get_min_y_idx(self.stationary)
        self.starting_point = PolyFunc.get_min_y_pt(self.stationary)

        self.locus_index = PolyFunc.get_max_y_idx(self.sliding)

        self.compute_nfp()
    
    def compute_nfp(self):
        """
        Main method for computing nfp of two polygons.
        """

        max_iterations: int = 75

        i = 0
        while not self.reached_end() and i < max_iterations:
            touching_edges: List[Intersection] = NFP.get_all_intersections(self.stationary, self.sliding)

            potential_vectors = self.get_potential_vectors(touching_edges)
            if not potential_vectors: 
                break

            feasible_vector = self.get_feasible_vector(touching_edges, potential_vectors)
            if not feasible_vector:
                break

            trimmed_vector = self.trim_vector(feasible_vector)
            if trimmed_vector == [0, 0]:
                break

            self.slide_polygon(trimmed_vector)
            self.nfp.append(list(self.sliding[self.locus_index]))
            i += 1

            if Polygon(self.sliding).intersects(Polygon(self.stationary)):
                break

        if i == max_iterations:
            self.error = -1 # add enum

    def reached_end(self) -> bool:
        """
        Locus index of sliding polygon equal to starting point (full loop completed).
        """
        return NFP._almost_equal(self.sliding[self.locus_index], self.starting_point)
    
    @staticmethod
    def get_all_intersections(p1: polyAsList, p2: polyAsList) -> List[Intersection]:
        """
        Returns list of TouchingEdge objects describing nature of found intersections. 
        """
        touching_edges = []
        stationary_edges: List[lineAsList] = NFP.get_all_edges(p1)
        sliding_edges: List[lineAsList] = NFP.get_all_edges(p2)
        for edge1 in stationary_edges: # optimize this trash complexity
            for edge2 in sliding_edges:
                intersection_pt: pointAsTuple = NFP.get_intersection(edge1, edge2)
                if intersection_pt is None: 
                    continue
                edge1_start: bool = NFP._almost_equal(edge1[0], intersection_pt)
                edge2_start: bool = NFP._almost_equal(edge2[0], intersection_pt)
                edge1_end: bool = NFP._almost_equal(edge1[1], intersection_pt) 
                edge2_end: bool = NFP._almost_equal(edge2[1], intersection_pt) 
                intersection_obj = Intersection(edge1, edge2, NFP.edge_to_vector(edge1), NFP.edge_to_vector(edge2), edge1_start, edge2_start, edge1_end, edge2_end, intersection_pt)
                touching_edges.append(intersection_obj)
        return touching_edges

    @staticmethod
    def get_potential_vectors(touching_edges: List[Intersection]):
        """
        Determine possible translation vectors.
        """
        all_vectors = []
        for touching in touching_edges:
            aim_edge = []
            line_rel = NFP.judge_position(touching.edge1, touching.edge2)
            
            # intersection at starting point of both edges
            if touching.edge1_start and touching.edge2_start:
                aim_edge = [touching.edge2[1], touching.edge2[0]] if line_rel == LineRelationship.ccw else touching.edge1

            # interesction at starting point of static edge
            elif touching.edge1_start:
                aim_edge = touching.edge1 if line_rel == LineRelationship.ccw else []
            
            # interesction at starting point of orbital edge
            elif touching.edge2_start:
                line_rel = NFP.judge_position(touching.edge2, touching.edge1)
                aim_edge = [touching.edge2[1], touching.edge2[0]] if line_rel == LineRelationship.cw else []

            # intersection none or somewhere in between ??
            else:
                aim_edge = touching.edge1 if line_rel == LineRelationship.ccw else []

            if aim_edge:
                vector = NFP.edge_to_vector(aim_edge)
                if vector not in all_vectors:
                    all_vectors.append(vector)

        return all_vectors
    
    @staticmethod
    def get_feasible_vector():
        pass

    @staticmethod
    def trim_vector():
        min_distance = float('inf')
        for edge in 

    @staticmethod
    def edge_to_vector(edge: lineAsList) -> pointAsTuple:
        """
        Turns a line into vector form.
        """
        return (edge[1][0] - edge[0][0], edge[1][1] - edge[0][1])

    @staticmethod
    def get_all_edges(p: polyAsList) -> List:
        """
        Turns polygon into list of edges.
        """
        return [[p[i], p[i+1%len(p)]] for i, _ in enumerate(p)]

    @staticmethod 
    def get_intersection(edge1: lineAsList, edge2: lineAsList) -> Union[None, pointAsTuple]:
        """
        Returns coordinates of intersection if it exists, None if it does not.
        """
        edge1, edge2 = LineString(edge1), LineString(edge2)
        intersection = edge1.intersection(edge2)
        if intersection.is_empty:
            return None
        return tuple(intersection.coords)[0]

    @staticmethod
    def judge_position(edge1: lineAsList, edge2: lineAsList) -> LineRelationship:
        """
        Determine if edge1 is ccw, cw, or parallel relative to edge2.
        """
        v1 = NFP.edge_to_vector(edge1)
        v2 = NFP.edge_to_vector(edge2)
        cross_product = NFP.cross_product(v1, v2)
        return {
            cross_product > 0: LineRelationship.ccw,
            cross_product < 0: LineRelationship.cw,
        }.get(True, LineRelationship.parallel)

    @staticmethod
    def _almost_equal(p1: polyAsList, p2: polyAsList, tolerance: float = 1e-6) -> bool:
        """
        Checks if x and y coordinates are within a certain threshold.
        """
        return abs(p1[0] - p2[0]) < tolerance and abs(p1[1] - p2[1]) < tolerance
