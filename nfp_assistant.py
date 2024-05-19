import os
import copy
from shapely.geometry import Polygon

from point_func import PointFunc
from poly_func import PolyFunc

from typing import List, Tuple, Any
from custom_types import polyAsList


class NFPAssistant:

    """
    Stores data for optimizing NFP generation process.
    """

    def __init__(self, polygons: List[polyAsList], store_nfp=False, store_path=None, get_all_nfp=False):

        self.polygons = self.delete_redundancy(copy.deepcopy(polygons))

        self.area_list: List[int] = []
        self.first_vec_list: List[List[float]] = []
        self.centroid_list: List[tuple] = []

        # save polygons by area, first vector, and centroid
        for poly_list in polygons:
            poly = Polygon(poly_list)
            self.centroid_list.append(PointFunc.point_as_tuple(poly.centroid))
            self.area_list.append(int(poly.area)) 
            self.first_vec_list.append(PolyFunc.get_first_vec(poly))

        # store list of nfps for impoved calculation time
        self.nfp_list = [[0] * len(self.polygons) for _ in range(len(self.polygons))]

        self.store_nfp = store_nfp
        self.store_path = store_path

        if get_all_nfp:
            self.get_all_nfp()

    @staticmethod
    def delete_redundancy(polys: List[polyAsList]) -> List[polyAsList]:
        unique_polys = []
        for poly in polys:
            if poly not in unique_polys:
                unique_polys.append(poly)
        return unique_polys

    def get_poly_index(self, target: polyAsList) -> int:
        """
        Gets index of polygon from list based on area and first vector if multiple of same area are found
        """
        area = int(Polygon(target).area)
        first_vec = PolyFunc.get_first_vec(Polygon(target))
        area_indices = NFPAssistant._get_index_multi(area, self.area_list) 

        if len(area_indices) == 1:
            return area_indices[0]
        
        vec_indices = NFPAssistant._get_index_multi(first_vec, self.first_vec_list)
        index = [x for x in area_indices if x in vec_indices]

        return index[0] if len(index) > 0 else -1

    @staticmethod
    def _get_index_multi(target: Any, list: List[Any]) -> List[int]:
        res = []
        for i, item in enumerate(list):
            if item == target:
                res.append(i)
        return res

    def get_all_nfp(self):
        for i, poly1 in enumerate(self.polygons):
            for j, poly2 in enumerate(self.polygons):
                nfp = NFP(poly1, poly2).nfp
                self.nfp_list[i][j] = PolyFunc.shift_poly(nfp, -self.centroid_list[i][0], -self.centroid_list[i][1])

    def get_direct_nfp(self, poly1: polyAsList, poly2: polyAsList):
        i = self.get_poly_index(poly1)
        j = self.get_poly_index(poly2)
        centroid = PointFunc.point_as_tuple(Polygon(poly1).centroid)

        if self.nfp_list[i][j] == 0:
            nfp = NFP(poly1, poly2).nfp
            return nfp

        return PolyFunc.shift_poly(self.nfp_list[i][j], centroid[0], centroid[1])

    def get_direct_nfp(self, poly1: polyAsList, poly2: polyAsList):
        i = self.get_poly_index(poly1)
        j = self.get_poly_index(poly2)
        centroid = PointFunc.point_as_tuple(Polygon(poly1).centroid)
        
