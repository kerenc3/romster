from cgshop2025_pyutils.data_schemas.instance import Cgshop2025Instance
from cgshop2025_pyutils.data_schemas.solution import Cgshop2025Solution
from cgshop2025_pyutils.geometry import Point, Segment, Polygon, ConstrainedTriangulation

class OrthogonalSolver:
    def __init__(self, instance: Cgshop2025Instance):
        self.instance = instance

    def solve(self) -> Cgshop2025Solution:
        instance = self.instance
        points = [Point(x, y) for x, y in zip(instance.points_x, instance.points_y)]

        # Generate rectangles from the polygon
        rectangles, steiner_points = self._divide_into_rectangles(points, instance.region_boundary)

        # Triangulate rectangles
        ct = ConstrainedTriangulation()
        point_indices = {point: ct.add_point(point) for point in points + steiner_points}
        edges = []

        for rect in rectangles:
            rect_edges = self._triangulate_rectangle(rect, ct, point_indices)
            edges.extend(rect_edges)

        # Construct the solution
        steiner_points_x = [p.x().exact() for p in steiner_points]
        steiner_points_y = [p.y().exact() for p in steiner_points]
        edge_indices = [(point_indices[e[0]], point_indices[e[1]]) for e in edges]

        return Cgshop2025Solution(
            content_type="CG_SHOP_2025_Solution",
            instance_uid=instance.instance_uid,
            steiner_points_x=steiner_points_x,
            steiner_points_y=steiner_points_y,
            edges=edge_indices,
        )

    def _divide_into_rectangles(self, points, boundary):
        """
        Divide the polygon into rectangles. This step assumes the input polygon
        is orthogonal (axis-aligned edges).

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

        rectangles = []
        steiner_points = []

        # Placeholder: Divide into rectangles by adding Steiner points (simplified logic)
        min_x = min(p.x() for p in boundary_points)
        max_x = max(p.x() for p in boundary_points)
        min_y = min(p.y() for p in boundary_points)
        max_y = max(p.y() for p in boundary_points)

        for x in range(int(min_x.exact()) + 1, max_x):
            for y in range(min_y + 1, max_y):
                steiner_points.append(Point(x, y))

        for i in range(0, len(boundary_points) - 1, 4):
            rectangles.append(boundary_points[i:i + 4])

        return rectangles, steiner_points

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
