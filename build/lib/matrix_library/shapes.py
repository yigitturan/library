from matplotlib.path import Path
from matrix_library import utils
import numpy as np
import math
from skimage.draw import polygon, disk
import os

# load pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Init some variables to reduce overhead
empty_canvas = np.zeros((128 * 128), dtype=bool)


# ✅ instead of path , using ray casting algorthm
def ray_casting_contains_points(points: np.ndarray, vertices: np.ndarray) -> np.ndarray:
    """
    Ray-Casting algoritmasını kullanarak verilen noktaların çokgen içinde olup olmadığını belirler.

    Parameters:
    - points (np.ndarray): Test edilecek noktalar, her nokta [x, y] formatında.
    - vertices (np.ndarray): Çokgenin köşe noktaları [x, y] formatında.

    Returns:
    - np.ndarray: Her noktanın çokgen içinde olup olmadığını belirten boolean dizisi.
    """
    result = np.zeros(len(points), dtype=bool)

    for i, (px, py) in enumerate(points):
        crossings = 0
        for j in range(len(vertices)):
            v1 = vertices[j]
            v2 = vertices[(j + 1) % len(vertices)]

            # Yüksekliği kontrol et ve doğru kesişim olup olmadığını belirle
            if ((v1[1] > py) != (v2[1] > py)) and \
                    (px < v1[0] + (py - v1[1]) * (v2[0] - v1[0]) / (v2[1] - v1[1])):
                crossings += 1

        result[i] = crossings % 2 == 1

    return result



class Polygon:
    def __init__(self, vertices: list, color: tuple = (255, 255, 255)):
        """
        Initializes a Polygon object with the given vertices and color.

        Parameters:
        - vertices (list): A list of vertices that define the polygon. Must have at least 3 vertices.
        - color (tuple, optional): The color of the polygon. Defaults to (255, 255, 255).

        Raises:
        - ValueError: If the number of vertices is less than 3.
        """
        if len(vertices) < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        self.vertices = np.array(vertices)
        self.color = color
        # that code deleted ( no path) self.path = Path(self.vertices)
        self.center = self.calculate_center()

    def contains_points(self, points: np.ndarray) -> np.ndarray:
       # """Check if the given points are inside the polygon."""
       #return self.path.contains_points(points)
       # ray casting alghoritm instead of path 
        return ray_casting_contains_points(points, self.vertices) 

    def translate(self, dx: float, dy: float) -> None:
        """
        Translate the polygon by a specified distance along the x and y axes.

        Parameters:
        - dx (float): The distance to translate along the x-axis.
        - dy (float): The distance to translate along the y-axis.
        """
        """
        self.vertices += np.array([dx, dy])
        self.update_path()
        self.center = (self.center[0] + dx, self.center[1] + dy)
        """
      #ray casting algorithm instead of path 
        self.vertices += np.array([dx, dy])
        self.center = (self.center[0] + dx, self.center[1] + dy)


    def rotate(self, angle_degrees: float, center: tuple = (0, 0)) -> None:
        """
        Rotate the polygon by a specified angle around a given center.

        Parameters:
        - angle_degrees (float): The angle by which to rotate the polygon (in degrees).
        - center (tuple, optional): The center of rotation (default is (0, 0)).
        """
        angle_radians = np.radians(angle_degrees)
        cos_angle = np.cos(angle_radians)
        sin_angle = np.sin(angle_radians)

        # Rotate each vertex
        rotated_vertices = []
        for x, y in self.vertices:
            # Translate point to origin
            x_translated = x - center[0]
            y_translated = y - center[1]

            # Apply rotation
            x_rotated = x_translated * cos_angle - y_translated * sin_angle
            y_rotated = x_translated * sin_angle + y_translated * cos_angle

            # Translate point back
            rotated_vertices.append((x_rotated + center[0], y_rotated + center[1]))

        self.vertices = np.array(rotated_vertices)
        
        ## deleted - self.update_path()

    ## deleted 
    
    #def update_path(self) -> None:
      #  """Update the path of the polygon based on its current vertices."""
      #  self.path = Path(self.vertices)

    def calculate_center(self) -> tuple:
        """Calculate the centroid of the polygon."""
        n = len(self.vertices)
        if n < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        cx, cy = 0.0, 0.0
        area = 0.0

        # Calculate the signed area and centroid
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            a = x1 * y2 - x2 * y1
            area += a
            cx += (x1 + x2) * a
            cy += (y1 + y2) * a

        area *= 0.5
        if area == 0:
            raise ValueError("Area of the polygon is zero.")

        cx /= 6 * area
        cy /= 6 * area

        return (cx, cy)

"""""
 def get_polygon_mask(self, shape: tuple) -> np.ndarray:
     #  """
     #  Create a binary mask for the polygon on a given image shape.

    #  Parameters:
     # - shape (tuple): The shape of the image (height, width).

    #  Returns:
    #  - mask (numpy.ndarray): A binary mask with the polygon filled in.
    #   """
    #  rr, cc = polygon(self.vertices[:, 1], self.vertices[:, 0], shape=shape)
     #  mask = np.zeros(shape, dtype=bool)
     # mask[rr, cc] = True
    # return mask
""""""
"""""
    def get_center(self) -> tuple:
        # Initialize sums for x and y coordinates
        sum_x = sum_y = 0

        # Loop through each vertex (assumed as a tuple (x, y))
        for x, y in self.vertices:
            sum_x += x
            sum_y += y

        # Calculate the averages of the x and y coordinates
        centroid_x = sum_x / len(self.vertices)
        centroid_y = sum_y / len(self.vertices)

        return (centroid_x, centroid_y)
"""""
"""""
def get_polygon_vertices(sides: int, radius: float = 1, center: tuple = (0, 0)) -> list:
    
    Calculate the vertices of a regular polygon.

    Parameters:
    - sides: Number of sides of the polygon.
    - radius: Radius of the circumcircle of the polygon (default is 1).
    - center: Tuple (x, y) representing the center of the polygon (default is (0, 0)).

    Returns:
    - A list of tuples representing the vertices of the polygon.
    
    if sides < 3:
        raise ValueError("A polygon must have at least 3 sides")

    vertices = []
    angle_step = 2 * math.pi / sides

    for i in range(sides):
        angle = i * angle_step
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append((x, y))

    return vertices
"""""

class Circle:
    def __init__(self, radius: float, center: tuple, color: tuple = (255, 255, 255)) -> None:
        """
        Initializes a Circle object with the given center, radius, and color.

        Parameters:
        - center (tuple): The (x, y) coordinates of the circle's center.
        - radius (float): The radius of the circle.
        - color (tuple, optional): The color of the circle. Defaults to (255, 255, 255).
        """
        if radius <= 0:
            raise ValueError("Radius must be greater than zero.")

        self.center = np.array(center)
        self.radius = radius
        self.color = color

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        """Ray-Casting yerine Euclidean mesafe ile kontrol"""
        distances = np.linalg.norm(points - self.center, axis=1)
        return distances <= self.radius

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        """Check if the given points are inside the circle."""
        distances = np.linalg.norm(points - self.center, axis=1)
        return distances <= self.radius

    


class Line(Polygon):
    def __init__(self, start: list, end: list, color: list = (255, 255, 255), thickness: float = 0.5) -> None:
        if start == end:
            raise ValueError("The start and end points of a line cannot be the same.")
        if thickness <= 0:
            raise ValueError("The thickness of a line must be greater than 0.")
        if len(start) != 2 or len(end) != 2:
            raise ValueError("The start and end points must be list of length 2.")
        if len(color) != 3:
            raise ValueError("The color must be a list of length 3.")

        self.start = np.array(start)
        self.end = np.array(end)
        self.thickness = thickness

        # ✅ Path kaldırıldı, sadece çizgi uç noktaları saklanıyor
        self.vertices = [self.start, self.end]

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        """Ray-Casting yerine çizgi üzerindeki mesafe kontrolü"""
        vec = self.end - self.start
        length = np.linalg.norm(vec)
        vec = vec / length if length != 0 else vec  # Normalize vektör

        proj = np.dot(points - self.start, vec)
        proj_clamped = np.clip(proj, 0, length)

        closest_points = self.start + proj_clamped[:, None] * vec
        distances = np.linalg.norm(points - closest_points, axis=1)
        return distances <= self.thickness