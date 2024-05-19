import os
import csv
import ast

from typing import List
from custom_types import polyAsList

class PolyReader:
    """
    Functional class for reading polygons from CSV files.

    ### CSV data format: 
    "[[x1, y1], [x2, y2], [x3, y3]]" // p1 \n
    "[[x1, y1], [x2, y2], [x3, y3], ... ,[xN, yN]]" // p2 \n
    """

    @staticmethod
    def read_polygons_from_csv(filepath: str) -> List[polyAsList]:
        """
        Reads CSV file containing a list of polygons and outputs a list of polygons stored as lists.

        Parameters:
        - filepath: path of CSV file.

        Returns:
        List of polygons stored as lists.

        Raises:
        - FileNotFoundError if filepath is invalid.
        - ValueError if file is of wrong type.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Invalid file path {filepath}")
        if os.path.splitext(filepath)[1] != '.csv':
            raise ValueError(f"Invalid file type for {filepath}")

        polygons = []

        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                polygons.append(PolyReader._eval_poly_string(row[0]))  
        
        return polygons

    @staticmethod
    def _eval_poly_string(poly_str: str) -> polyAsList:
        """
        Evaluates list stored as a string.

        Parameters:
        - poly_str: polygon as a list stored in string form.

        Returns:
        Polygon stored in list form.
        """
        return ast.literal_eval(poly_str)
    