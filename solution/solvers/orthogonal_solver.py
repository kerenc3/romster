import math
from itertools import product

from cgshop2025_pyutils.data_schemas.instance import Cgshop2025Instance
from cgshop2025_pyutils.data_schemas.solution import Cgshop2025Solution
from cgshop2025_pyutils.geometry import Point, Segment, Polygon, ConstrainedTriangulation
from matplotlib import pyplot as plt

from cgshop2025_pyutils import (
    DelaunayBasedSolver,
    InstanceDatabase,
    ZipSolutionIterator,
    ZipWriter,
    verify,
    visualization,
    VerificationResult
)

from shapely import ops, geometry



class OrthogonalSolver:
    def __init__(self, instance: Cgshop2025Instance):
        self.instance = instance

    def solve(self) -> Cgshop2025Solution:
        ct = ConstrainedTriangulation()
        instance = self.instance
        instance_points = []
        for x, y in zip(instance.points_x, instance.points_y):
            ct.add_point(Point(x, y))
            instance_points.append(Point(x,y))
        ct.add_boundary(instance.region_boundary)
        for constraint in instance.additional_constraints:
            ct.add_segment(constraint[0], constraint[1])

        polygon = Polygon(instance_points)

        potential_points =  set(product(instance.points_x, instance.points_y))

        romsters = []
        for p in potential_points:
            point = Point(p[0], p[1])
            if point not in instance_points and (polygon.contains(point) or polygon.on_boundary(point)):
                romsters.append(p)



            # Visualize the instance and solution
            # Create a plot
        fig, ax = plt.subplots(figsize=(10, 8))

        points_x = instance.points_x
        points_y = instance.points_y
        # Plot the points
        #
        rom_x = []
        rom_y = []
        for p in romsters:
            print(p)
            rom_x.append(p[0])
            rom_y.append(p[1])

        # # Create a polygon
        # all_x = points_x + rom_x
        # all_y = points_y + rom_y
        # ears_points = []
        # for i, x in enumerate(all_x):
        #     ears_points.append((all_x[i], all_y[i]))
        # polygon = geometry.Polygon(ears_points)
        # # Triangulate the polygon
        # triangles = ops.triangulate(polygon)
        # # Plot the triangles
        # fig, ax = plt.subplots()
        # for triangle in triangles:
        #     x, y = triangle.exterior.xy
        #     ax.fill(x, y, alpha=0.5, fc='orange', ec='black')
        #     # Plot the original polygon for reference
        # x, y = polygon.exterior.xy
        # ax.plot(x, y, color='blue', label='Original Polygon')
        # ax.legend()
        # ax.set_aspect('equal')
        # plt.show()
        # ax.scatter(points_x, points_y, color='blue')
        # ax.scatter(rom_x, rom_y, color='green')

        # Add index labels near each point
        for i, (x, y) in enumerate(zip(points_x, points_y)):
            ax.text(x, y, str(i), fontsize=12, ha='right', color='red')

        # Set axis labels and title
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Instance Plot with Indices")

        # Plot the instance using the provided function
        ax = visualization.plot_instance(ax, instance)

        # Finalize plot with legend and show
        # ax.legend()

        plt.show()

        plt.close()

        edges = ct.get_triangulation_edges()
        return Cgshop2025Solution(
            instance_uid=instance.instance_uid,
            steiner_points_x=[],
            steiner_points_y=[],
            edges=edges,
        )
    # def __init__(self, instance: Cgshop2025Instance):
    #     self.instance = instance
    #
    # def solve(self) -> Cgshop2025Solution:
    #     print("nosh")
    #     ct = ConstrainedTriangulation()
    #     instance_points = []
    #     instance = self.instance
    #     for x, y in zip(instance.points_x, instance.points_y):
    #         instance_points.append(Point(x,y))
    #
    #     print("nosh2")
    #     ct.add_boundary(instance.region_boundary)
    #     print("nosh2")
    #     for constraint in instance.additional_constraints:
    #         ct.add_segment(constraint[0], constraint[1])
    #
    #     polygon = Polygon(instance_points)
    #
    #     print("nosh2")
    #     # potential_points =  set(product(instance.points_x, instance.points_y))
    #     #
    #     # romsters = []
    #     # for p in potential_points:
    #     #     if Point(p) not in instance_points and (polygon.contains(Point(p)) or polygon.on_boundary(Point(p))):
    #     #         romsters.append(p)
    #     #
    #     # for p in romsters:
    #     #     ct.add_point(Point(p))
    #
    #     edges = ct.get_triangulation_edges()
    #
    #     # print("edges:")
    #     # print(edges)
    #
    #     return Cgshop2025Solution(
    #         instance_uid=instance.instance_uid,
    #         steiner_points_x=[],
    #         steiner_points_y=[],
    #         edges=edges,
    #     )

        # # Initialize lists for x and y coordinates of Steiner points
        # steiner_points_x = []
        # steiner_points_y = []
        #
        # # Loop through all vertices (exclude boundary vertices to find Steiner points)
        # boundary_vertices = set([idx for edge in boundary_edges for idx in edge])
        #
        # for idx, point in enumerate(steiner_points):
        #     if idx not in boundary_vertices:
        #         # For each Steiner point, process the x and y coordinates into the desired format
        #         x = point[0]
        #         y = point[1]
        #
        #         # Convert x and y to fraction form or integer form
        #         x_value = str(Fraction(x).limit_denominator()) if not x.is_integer() else int(x)
        #         y_value = str(Fraction(y).limit_denominator()) if not y.is_integer() else int(y)
        #
        #         steiner_points_x.append(x_value)
        #         steiner_points_y.append(y_value)
        # print(edges)
        # return Cgshop2025Solution(
        #     instance_uid=instance.instance_uid,
        #     steiner_points_x=steiner_points_x,
        #     steiner_points_y=steiner_points_y,
        #     edges=edges,
        # )



    def _divide_into_rectangles(self, points, boundary):
        """
        Divide the polygon into rectangles. Steiner points are added across vertices
        with angles greater than 90 degrees to ensure proper division.

        Args:
            points: List of Point objects.
            boundary: List of indices representing the boundary of the polygon.

        Returns:
            rectangles: List of rectangles as lists of Point objects.
            steiner_points: List of Steiner points added during the division.
        """
        boundary_points = [points[i] for i in boundary]
        polygon = Polygon(boundary_points)

        if not polygon.is_simple():
            raise ValueError("Input polygon is not simple.")

        print("Polygon is simple and valid.")
        steiner_points = []

        for i, point in enumerate(boundary_points):
            prev_point = boundary_points[i - 1]
            next_point = boundary_points[(i + 1) % len(boundary_points)]

            angle = self._calculate_angle(prev_point, point, next_point)
            print(f"Vertex {i}: angle={angle}")

            if angle > 90:
                # Add Steiner points to split the angle appropriately
                if angle <= 180:
                    steiner_point = self._add_steiner_point_across(point, prev_point, next_point)
                    steiner_points.append(steiner_point)
                elif angle > 180:
                    steiner_point1 = self._add_steiner_point_across(point, prev_point, next_point)
                    steiner_point2 = self._add_steiner_point_across(point, next_point, prev_point)
                    steiner_points.extend([steiner_point1, steiner_point2])

        return [boundary_points], steiner_points

    def _calculate_angle(self, p1, p2, p3):
        """
        Calculate the angle at point p2 formed by p1-p2-p3.

        Args:
            p1: Previous Point.
            p2: Current Point.
            p3: Next Point.

        Returns:
            The angle in degrees.
        """
        v1 = (int((p1.x() - p2.x()).exact()), int((p1.y() - p2.y()).exact()))
        v2 = (int((p3.x() - p2.x()).exact()), int((p3.y() - p2.y()).exact()))

        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        mag_v1 = (v1[0]**2 + v1[1]**2)**0.5
        mag_v2 = (v2[0]**2 + v2[1]**2)**0.5

        cos_angle = dot_product / (mag_v1 * mag_v2)
        angle = math.degrees(math.acos(cos_angle))

        return angle

    def _add_steiner_point_across(self, vertex, edge_start, edge_end):
        """
        Add a Steiner point across the vertex to split the angle.

        Args:
            vertex: The vertex with a large angle.
            edge_start: Start of the edge.
            edge_end: End of the edge.

        Returns:
            A Steiner Point.
        """
        mid_x = int((edge_start.x() + edge_end.x()).exact()) / 2
        mid_y = int((edge_start.y() + edge_end.y()).exact()) / 2

        steiner_point = Point(mid_x, mid_y)
        print(f"Added Steiner point at ({mid_x}, {mid_y})")
        return steiner_point

    def _triangulate_rectangle(self, rect, ct, point_indices):
        """
        Triangulate a single rectangle into non-acute triangles.

        Args:
            rect: A list of 4 Point objects representing the rectangle.
            ct: A ConstrainedTriangulation instance.
            point_indices: A dictionary mapping Point objects to their indices in the triangulation.

        Returns:
            edges: List of edges of the triangulation as tuples of Point objects.
        """
        print(f"Triangulating rectangle with corners: {[p.exact() for p in rect]}")
        p1, p2, p3, p4 = rect

        # Add edges of the rectangle
        ct.add_segment(point_indices[p1], point_indices[p2])
        ct.add_segment(point_indices[p2], point_indices[p3])
        ct.add_segment(point_indices[p3], point_indices[p4])
        ct.add_segment(point_indices[p4], point_indices[p1])

        # Add diagonal to split rectangle into two triangles
        ct.add_segment(point_indices[p1], point_indices[p3])

        return [
            (p1, p2), (p2, p3), (p3, p4), (p4, p1), (p1, p3)
        ]
