import datetime
from typing import List, Union
from shapely.geometry import Polygon, MultiPolygon

from custom_types import polyAsList, pointAsTuple
from reader import PolyReader
from poly_func import PolyFunc
from nfp_assistant import NFPAssistant
from plt_util import PltUtil
from axis import Axis


class Borders:
    """
    Class to store and update borders of a container for packing 2D objects.

    ### Parameters:
    - left: left border of container
    - right: right border of container
    - top: top border of container
    - bottom: bottom border of container
    All input parameters are floating point values that default to zero

    ### Attributes:
    - left, right, top and bottom identical to input parameters
    - height and width computed using difference between top and bottom, right and left

    ### Examples:
    >>> b = Borders(20, 80, 100, 0)
    >>> b.update(0, 100, 120, 20)
    >>> b.height
    120
    """
    def __init__(self, left: float = 0, right: float = 0, top: float = 0, bottom: float = 0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self._update_dimensions()

    def update(self, left: float = 0, right: float = 0, top: float = 0, bottom: float = 0):
        """
        Update the bounding box coordinates.

        Parameters:
        - left: The left coordinate. Defaults to 0.
        - right: The right coordinate. Defaults to 0.
        - top: The top coordinate. Defaults to 0.
        - bottom: The bottom coordinate. Defaults to 0.
        """
        self.left = min(left, self.left)
        self.right = max(right, self.right)
        self.bottom = min(bottom, self.bottom)
        self.top = max(top, self.top)
        self._update_dimensions()

    def _update_dimensions(self):
        """
        Update the width and height of the bounding box.
        """
        self.width = self.right - self.left
        self.height = self.top - self.bottom

class TOPOS:

    """
    Top-Left Overlap Search

    Main method:
    - Add first polygon to packing area, initialize bounds of current arrangement.
    - 

    Helper methods:
    update_bounds - updates outer boundary of current polygons
    choose_feasible_point - selects feasible points based on current state
    slide_to_bottom_left - slides polygons to bottom-left corner to optimize layout
    show_result - plots final result of packing 

    """

    def __init__(self, polygons: List[polyAsList], container_width: float):
        self.polys: List[polyAsList] = polygons
        self.active_polys: List[polyAsList] = []
        self.width: float = container_width
        self.NFPAssistant = NFPAssistant(self.polys, store_nfp=False, get_all_nfp=True, load_history=True)  
        self.execute()

    '''
    todo: 
    NFPAssistant.getDirectNFP
    '''
    def execute(self):
        self.active_polys.append(self.polys[0])  
        self.borders = Borders()

        for curr_poly in self.polys[1:]:
            curr_poly_shapely = Polygon(curr_poly)

            self.update_bounds()

            # Polygon if contiguous, MultiPolygon otherwise.
            feasible_border: Union[Polygon, MultiPolygon] = Polygon(self.active_polys[0])

            for fixed_poly in self.active_polys:
                nfp = self.NFPAssistant.get_direct_nfp(fixed_poly, curr_poly)
                feasible_border = feasible_border.union(Polygon(nfp))

            feasible_points: List[pointAsTuple] = self.get_feasible_points(feasible_border)

            left_pt = PolyFunc.get_min_x_pt(curr_poly_shapely)
            top_pt = PolyFunc.get_max_y_pt(curr_poly_shapely)
            right_pt = PolyFunc.get_max_x_pt(curr_poly_shapely)

            left_top_x_diff: float = top_pt[Axis.x] - left_pt[Axis.x]
            right_top_x_diff: float = right_pt[Axis.x] - top_pt[Axis.x]

            min_change: float = float('inf')
            target_point: pointAsTuple = []

            for point in feasible_points:
                
                x, y = point

                change: float = min_change

                if x - left_top_x_diff > self.borders.left and x + right_top_x_diff <= self.borders.right:
                    change = self.borders.left - x
                elif min_change > 0:
                    change = max(self.borders.left - x + left_top_x_diff, x + right_top_x_diff - self.borders.right)

            if change < min_change:
                min_change = change
                target_point = point

            reference_point = curr_poly[PolyFunc.get_max_y_pt(curr_poly)]
            self.active_polys.append(PolyFunc.shift_poly(curr_poly, target_point[Axis.x] - reference_point[Axis.x], target_point[Axis.y] - reference_point[Axis.y]))

        self.slide_to_bottom_left()
        self.show_result()

    def update_bounds(self):
        """
        Change bounds based on added polygon.
        """
        left, bottom, right, top = self.active_polys[-1].bounds
        self.borders.update(left=left, right=right, top=top, bottom=bottom)

    def get_feasible_points(self, border: Union[Polygon, MultiPolygon]) -> List[pointAsTuple]:
        """
        Get all points in border within bounds of border box.
        """
        res = []

        if border.isinstance(Polygon):
            res.append(TOPOS.get_feasible_points_poly(border))
            return res
        
        for poly in border:
            res.append(TOPOS.get_feasible_points_poly(poly))

        return res

    def get_feasible_points_poly(self, poly: Polygon) -> List[pointAsTuple]:
        """
        Get all points in polygon within bounds of border box.
        """
        res = []

        for point in poly.exterior.coords:
            x, y = point

            between_top_bottom: bool = self.borders.bottom < y < self.borders.top
            within_width: bool = self.borders.left < x < self.borders.right

            if between_top_bottom and within_width:
                res.append((x, y))

        return res

    def slide_to_bottom_left(self):
        """
        Shift all placed polygons to bottom left of container.
        """
        for poly in self.active_polys:
            PolyFunc.shift_poly(poly, -self.border.left, -self.border.right)

    def show_result(self):
        """
        Display result using plotting util.
        """
        for poly in self.active_polys:
            PltUtil.add_polygon(poly)
        PltUtil.show_plot()

if __name__=='__main__':
    starttime = datetime.datetime.now()
    data: List[polyAsList] = PolyReader.read_polygons_from_csv('blaz.csv')  
    app = TOPOS(data, 1000)  
    endtime = datetime.datetime.now()
    print ("total time: ",endtime - starttime)