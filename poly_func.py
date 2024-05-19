import operator
from shapely.geometry import Polygon

from typing import Tuple, Union
from custom_types import pointAsTuple
from axis import Axis

class PolyFunc:
    
    """
    Functional class for performing operations on shapely polygons.
    """
    @staticmethod
    def get_min_x_pt(poly: Polygon) -> pointAsTuple:
        """
        Returns the point containing the minimum x value of the input polygon.

        Parameters:
        - poly: Shapely polygon.

        Returns:
        Point in the form of a tuple containing two floats.
        """
        PolyFunc._get_extreme(poly, Axis.x, min=True, idx=False)
    
    @staticmethod
    def get_max_x_pt(poly: Polygon) -> pointAsTuple:
        """
        Returns the point containing the maximum x value of the input polygon.

        Parameters:
        - poly: Shapely polygon.

        Returns:
        Point in the form of a tuple containing two floats.
        """
        PolyFunc._get_extreme(poly, Axis.x, min=False, idx=False)
    
    @staticmethod
    def get_min_y_pt(poly: Polygon) -> pointAsTuple:
        """
        Returns the point containing the minimum y value of the input polygon.

        Parameters:
        - poly: Shapely polygon.

        Returns:
        Point in the form of a tuple containing two floats.
        """
        PolyFunc._get_extreme(poly, Axis.y, min=True, idx=False)
    
    @staticmethod
    def get_max_y_pt(poly: Polygon) -> pointAsTuple:
        """
        Returns the point containing the maximum y value of the input polygon.

        Parameters:
        - poly: Shapely polygon.

        Returns:
        Point in the form of a tuple containing two floats.
        """
        PolyFunc._get_extreme(poly, Axis.y, min=False, idx=False)

    @staticmethod
    def get_min_x_idx(poly: Polygon) -> int:
        """
        Returns the index of the point containing the minimum x value of the input polygon.

        Parameters:
        - poly: Shapely polygon.

        Returns:
        Integer index.
        """
        PolyFunc._get_extreme(poly, Axis.x, min=True, idx=True)
    
    @staticmethod
    def get_max_x_idx(poly: Polygon) -> int:
        """
        Returns the index of the point containing the maximum x value of the input polygon.

        Parameters:
        - poly: Shapely polygon.

        Returns:
        Integer index.
        """
        PolyFunc._get_extreme(poly, Axis.x, min=False, idx=True)
    
    @staticmethod
    def get_min_y_idx(poly: Polygon) -> int:
        """
        Returns the index of the point containing the minimum y value of the input polygon.

        Parameters:
        - poly: Shapely polygon.

        Returns:
        Integer index.
        """
        PolyFunc._get_extreme(poly, Axis.y, min=True, idx=True)
    
    @staticmethod
    def get_max_y_idx(poly: Polygon) -> int:
        """
        Returns the index of the point containing the maximum y value of the input polygon.

        Parameters:
        - poly: Shapely polygon.

        Returns:
        Integer index.
        """
        PolyFunc._get_extreme(poly, Axis.y, min=False, idx=True)

    @staticmethod
    def _get_extreme(poly: Polygon, axis: int, min: bool, idx: bool) -> Union[int, pointAsTuple]:
        """
        Returns either point or index of point containing extreme x or y value.

        Parameters:
        - poly: Shapely polygon.
        - axis: x or y.
        - min: True for minimum, False for maximum value.
        - idx: True to return index, False to return point.

        Returns: 
        Index of extreme point or extreme point in the form of a tuple containing two floats.

        Raises:
        - ValueError if axis is invalid 
        """

        if axis not in Axis.__members__.values():
            raise ValueError(f"Invalid axis value {axis}")

        comparison_operator = operator.lt if min else operator.gt
        extreme_val: float = poly[0][axis]
        extreme_idx: int = 0

        for i, point in enumerate(poly):
            if comparison_operator(point[axis], extreme_val):
                extreme_val = point[axis]
                extreme_idx = i
        
        return extreme_idx if idx else poly[extreme_idx]
    
    @staticmethod
    def get_extreme_points(poly: Polygon) -> Tuple[pointAsTuple]:
        """
        Returns points that contain minimum and maximum x and y values of the input polygon

        Parameters:
        - poly: Shapely polygon

        Returns:
        Tuple of points stored as tuples containing two floats
        """
        return PolyFunc.get_min_x_pt(poly), PolyFunc.get_max_x_pt(poly), PolyFunc.get_min_y_idx(poly), PolyFunc.get_max_y_pt(poly)
    
    @staticmethod
    def get_first_vec(poly: Polygon) -> Tuple[float, float]:
        """
        Returns first vector of polygon

        Parameters:
        - poly: Shapely polygon

        Returns:
        2D vector in the form of a tuple consisting of two floats
        """
        return (poly[1][0] - poly[0][0], poly[1][1] - poly[0][1])

    @staticmethod
    def shift_poly(poly: Polygon, x: float, y: float) -> Polygon:
        """
        Returns input polygon shifted by the input vector

        Parameters:
        - poly: Shapely polygon

        Returns:
        Shifted polygon
        """
        shifted_points = [(point.x + x, point.y + y) for point in poly.exterior.coords]
        return Polygon(shifted_points)
