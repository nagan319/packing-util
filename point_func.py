from typing import Tuple
from shapely.geometry import Point
from custom_types import pointAsTuple

class PointFunc:

    """
    Functional class for performing operations on shapely points
    """
    
    @staticmethod
    def point_as_tuple(point: Point) -> pointAsTuple:
        """
        Returns tuple representation of shapely point object
        """
        return (point.x, point.y)
        