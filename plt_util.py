import os
import matplotlib.pyplot as plt

from custom_types import polyAsList, lineAsList

class PltUtil:
    """
    Utility class for interacting with matplotlib to visualize polygons and lines.
    """

    @staticmethod
    def add_polygon(poly: polyAsList):
        """
        Add a polygon to the plot.

        Parameters:
        - poly: A list of points representing the vertices of the polygon.
        """
        for i in range(len(poly)):
            if i == len(poly) - 1:
                PltUtil.add_line([poly[i], poly[0]])
            else:
                PltUtil.add_line([poly[i], poly[i+1]])

    @staticmethod
    def add_line(line: lineAsList):
        """
        Add a line to the plot.

        Parameters:
        - line: A list containing the start and end points of the line.
        """
        plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color="black", linewidth=.5)

    @staticmethod
    def show_plot(width: int = 1000, height: int = 1000):
        """
        Display the plot with specified width and height.

        Parameters:
        - width: Width of the plot.
        - height: Height of the plot.
        """
        plt.axis([0, width, 0, height])
        plt.show()
        plt.clf()

    @staticmethod
    def save_fig(name: str):
        """
        Save the current plot to a file.

        Parameters:
        - name: Name of the file to save the plot.
        """
        filename = name + '.png'
        if os.path.exists(filename):
            return
        plt.savefig(filename)
        plt.cla()
        