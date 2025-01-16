from collections import defaultdict

from cgshop2025_pyutils.geometry import Point, Segment, Polygon, ConstrainedTriangulation

from pyutils25.src.cgshop2025_pyutils import Cgshop2025Instance, Cgshop2025Solution
from solution.our_geometry import *


class DelaunayCopySolver:
    def __init__(self, instance: Cgshop2025Instance):
        self.instance = instance

    def solve(self) -> Cgshop2025Solution:
        ct = ConstrainedTriangulation()
        instance = self.instance
        for x, y in zip(instance.points_x, instance.points_y):
            ct.add_point(Point(x, y))
        ct.add_boundary(instance.region_boundary)
        for constraint in instance.additional_constraints:
            ct.add_segment(constraint[0], constraint[1])
        edges = ct.get_triangulation_edges()

        # print("edges:")
        # print(edges)

        return Cgshop2025Solution(
            instance_uid=instance.instance_uid,
            steiner_points_x=[],
            steiner_points_y=[],
            edges=edges,
        )

    def improve_step1(self, solution) -> Cgshop2025Solution:
        print("instance:")
        print(self.instance)
        print("solution:")
        print(solution)

        #### Figure out all triangles:
        # Create a dictionary to store all vertices connected to each vertex
        adjacency_list = defaultdict(set)

        # Populate adjacency list
        for edge in solution.edges:
            adjacency_list[edge[0]].add(edge[1])
            adjacency_list[edge[1]].add(edge[0])

        # Extract triangles
        triangles = set()
        for vertex in adjacency_list:
            neighbors = list(adjacency_list[vertex])
            # Check all pairs of neighbors to see if they are connected to each other
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if neighbors[j] in adjacency_list[neighbors[i]]:
                        # Sort and store the triangle as a sorted tuple of 3 points
                        triangle = tuple(sorted([vertex, neighbors[i], neighbors[j]]))
                        triangles.add(triangle)

        # Convert triangles to a list
        triangles_list = list(triangles)
        print(triangles_list)

        ### End

        points = list(zip(self.instance.points_x, self.instance.points_y))
        print("points")
        print(points)

        projection_points = []
        for triangle in triangles:
            a, b, c = points[triangle[0]], points[triangle[1]], points[triangle[2]]
            # if is_obtuse_by_sides(a, b, c):
            is_obtuse, longest_edge, opposite_vertex = is_obtuse_by_sides_and_longest_edge(a, b, c)
            if is_obtuse:
                print(triangle, " is obsute")
                projection = perpendicular_projection(opposite_vertex, longest_edge[0], longest_edge[1])
                # ax.scatter(projection[0], projection[1], color='red', zorder=5, label='Projection Point')
                projection_points.append((projection[0], projection[1]))

                # points_x.append(projection[0])
                # points_y.append(projection[1])
                # self.instance.add_point(Point(projection[0], projection[1]))

                # Print the projection point
                print(f"The perpendicular projection point is: {projection}")

            else:
                print(triangle, " is non-obsute")

        # print(projection_points)

        return solution, projection_points

    def improve_step1(self, solution) -> Cgshop2025Solution:
        # print("Instance:")
        # print(self.instance)
        # print("Solution:")
        # print(solution)

        #### Figure out all triangles:
        # Create a dictionary to store all vertices connected to each vertex
        adjacency_list = defaultdict(set)

        # Populate adjacency list
        for edge in solution.edges:
            adjacency_list[edge[0]].add(edge[1])
            adjacency_list[edge[1]].add(edge[0])

        # Extract triangles
        triangles = set()
        for vertex in adjacency_list:
            neighbors = list(adjacency_list[vertex])
            # Check all pairs of neighbors to see if they are connected to each other
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if neighbors[j] in adjacency_list[neighbors[i]]:
                        # Sort and store the triangle as a sorted tuple of 3 points
                        triangle = tuple(sorted([vertex, neighbors[i], neighbors[j]]))
                        triangles.add(triangle)

        # Convert triangles to a list
        triangles_list = list(triangles)
        # print(triangles_list)

        x_s_points = get_float_points(solution.steiner_points_x)
        y_s_points = get_float_points(solution.steiner_points_y)
        points = list(zip(self.instance.points_x, self.instance.points_y)) + list(zip(x_s_points, y_s_points))

        projection_points = []
        for triangle in triangles:
            # print(triangle)
            a, b, c = points[triangle[0]], points[triangle[1]], points[triangle[2]]
            # if is_obtuse_by_sides(a, b, c):
            is_obtuse, longest_edge, opposite_vertex = is_obtuse_by_sides_and_longest_edge(a, b, c)
            if is_obtuse:
                # print(triangle," is obsute")
                projection = perpendicular_projection(opposite_vertex, longest_edge[0], longest_edge[1])
                # ax.scatter(projection[0], projection[1], color='red', zorder=5, label='Projection Point')
                projection_points.append((projection[0], projection[1]))

                # points_x.append(projection[0])
                # points_y.append(projection[1])
                # self.instance.add_point(Point(projection[0], projection[1]))

                # Print the projection point
                # print(f"The perpendicular projection point is: {projection}")

            # else:
            # print(triangle," is non-obsute")

        # print(projection_points)

        return projection_points


    def improve_step2(self, projections) -> Cgshop2025Solution:
        ct = ConstrainedTriangulation()
        instance = self.instance
        for x, y in zip(instance.points_x, instance.points_y):
            ct.add_point(Point(x, y))
        for point in projections:
            ct.add_point(Point(point[0], point[1]))
        ct.add_boundary(instance.region_boundary)
        for constraint in instance.additional_constraints:
            ct.add_segment(constraint[0], constraint[1])
        edges = ct.get_triangulation_edges()

        return Cgshop2025Solution(
            instance_uid=instance.instance_uid,
            steiner_points_x=[],
            steiner_points_y=[],
            edges=edges,
        )



