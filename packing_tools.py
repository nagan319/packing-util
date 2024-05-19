from typing import List, Tuple
import numpy as np
from shapely.geometry import Polygon, Point

'''
    required direct imports from algo:
        PackingUtil <- bounding box impemented in polygon class
        PolyListProcessor <- will store majority of methods in polygon class, list will wrap them
'''

class GeoFunc:

    TOLERANCE: float = .01  # some arbitrary value

    @staticmethod
    def almost_contains(line: List[Point], pt: Point):
        delta: float = GeoFunc.TOLERANCE

        ptA = line[0]
        ptB = line[1]

        # Horizontal line
        if abs(ptA.y - pt.y) < delta and abs(ptB.y - pt.y) < delta:
            return (ptA.x - pt.x) * (ptB.x - pt.x) < 0

        # Vertical line
        if abs(ptA.x - pt.x) < delta and abs(ptB.x - pt.x) < delta:
            return (ptA.y - pt.y) * (ptB.y - pt.y) < 0

        if abs(ptA.x - pt.x) < delta or abs(ptB.x - pt.x) < delta or abs(ptA.x - ptB.x) < delta:
            return False

        # Usual condition, calculate angle difference
        arc1 = np.arctan((ptA.y - ptB.y) / (ptA.x - ptB.x))
        arc2 = np.arctan((pt.y - ptB.y) / (pt.x - ptB.x))

        if abs(arc2 - arc1) < delta:
            return (pt.y - ptA.y) * (ptB.y - pt.y) > 0 and (pt.x - ptA.x) * (ptB.x - pt.x) > 0
        else:
            return False




    