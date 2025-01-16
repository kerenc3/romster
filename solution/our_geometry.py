def squared_distance(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


# Check if a triangle is obtuse based on edge lengths
def is_obtuse_by_sides(a, b, c):
    # Compute squared distances (sides of the triangle)
    ab2 = squared_distance(a, b)
    bc2 = squared_distance(b, c)
    ca2 = squared_distance(c, a)

    # Sort squared distances to easily identify the longest side
    sides_squared = sorted([ab2, bc2, ca2])

    # Check the condition for obtuseness
    return sides_squared[0] + sides_squared[1] < sides_squared[2]


def is_obtuse_by_sides_and_longest_edge(a, b, c):
    # Compute squared distances (sides of the triangle)
    ab2 = squared_distance(a, b)
    bc2 = squared_distance(b, c)
    ca2 = squared_distance(c, a)

    # Sort squared distances to easily identify the longest side
    sides_squared = sorted([(ab2, (a, b)), (bc2, (b, c)), (ca2, (c, a))], key=lambda x: x[0])

    # Identify the longest edge and the opposite vertex
    longest_edge = sides_squared[2][1]
    if longest_edge == (a, b):
        opposite_vertex = c
    elif longest_edge == (b, c):
        opposite_vertex = a
    else:
        opposite_vertex = b

    # Check if the triangle is obtuse
    is_obtuse = sides_squared[0][0] + sides_squared[1][0] < sides_squared[2][0]

    return is_obtuse, longest_edge, opposite_vertex


def perpendicular_projection(A, B, C):
    # Coordinates of the points
    x1, y1 = A  # Opposite vertex
    x2, y2 = B  # First point of the longest edge
    x3, y3 = C  # Second point of the longest edge

    # Vector from B to C (the direction of the edge)
    BCx = x3 - x2
    BCy = y3 - y2

    # Vector from B to A
    BAx = x1 - x2
    BAy = y1 - y2

    # Dot product of vectors BA and BC
    dot_product = BAx * BCx + BAy * BCy

    # Squared length of vector BC (the edge)
    BC_squared = BCx ** 2 + BCy ** 2

    # Projection of point A onto the line BC
    proj_x = x2 + (dot_product / BC_squared) * BCx
    proj_y = y2 + (dot_product / BC_squared) * BCy

    return (proj_x, proj_y)


def get_float_points(org_points):
    points = []
    for p in org_points:
        if type(p) is str:
            if p.find('/'):
                mone, mechane = p.split('/')
                point = float(int(mone) / int(mechane))
            else:
                point = float(p)
        else:
            point = p
        points.append(point)
    return points


def center_of_mass(points):
    if not points:
        raise ValueError("The list of points is empty.")

    x_coords = [x for x, y in points]
    y_coords = [y for x, y in points]

    center_x = sum(x_coords) / len(points)
    center_y = sum(y_coords) / len(points)

    return center_x, center_y


import matplotlib.pyplot as plt
from shapely.geometry import Polygon, box
from shapely.ops import split
import numpy as np


def partition_polygon_to_rectangles(x_points, y_points):
    """
    Partitions a polygon described by x_points and y_points into rectangles.
    Prefers 'fat' rectangles when possible.

    :param x_points: List of x-coordinates of the polygon vertices.
    :param y_points: List of y-coordinates of the polygon vertices.
    :return: List of rectangles as (min_x, min_y, max_x, max_y).
    """
    # Create the polygon
    polygon = Polygon(zip(x_points, y_points))
    if not polygon.is_valid:
        raise ValueError("The provided polygon is invalid.")

    rectangles = []

    while not polygon.is_empty:
        # Calculate the bounding box of the polygon
        minx, miny, maxx, maxy = polygon.bounds

        # Choose the largest square-like rectangle
        width = maxx - minx
        height = maxy - miny
        side_length = min(width, height)  # To keep the rectangle "fat"

        # Create the rectangle
        rect = box(minx, miny, minx + side_length, miny + side_length)
        intersected_rect = polygon.intersection(rect)

        # Ensure the rectangle is within the polygon
        if not intersected_rect.is_empty:
            rectangles.append(intersected_rect.bounds)
            polygon = polygon.difference(intersected_rect)
        else:
            break  # If no valid rectangle can be created, stop

    return rectangles


def plot_partition(x_points, y_points, rectangles):
    """
    Plots the original polygon and its rectangle partitioning.
    """
    # Plot the original polygon
    plt.figure(figsize=(8, 8))
    plt.plot(x_points + [x_points[0]], y_points + [y_points[0]], label='Polygon', color='blue')

    # Plot the rectangles
    for rect in rectangles:
        minx, miny, maxx, maxy = rect
        plt.fill([minx, maxx, maxx, minx, minx], [miny, miny, maxy, maxy, miny],
                 edgecolor='red', facecolor='none', linestyle='--', label='Rectangle')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.show()

# # Example usage
# x_points = [0, 5, 5, 2, 2, 0]
# y_points = [0, 0, 5, 5, 3, 3]

# rectangles = partition_polygon_to_rectangles(x_points, y_points)
# print("Rectangles:", rectangles)

# plot_partition(x_points, y_points, rectangles)