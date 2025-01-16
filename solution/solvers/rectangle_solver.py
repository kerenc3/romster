from cgshop2025_pyutils.data_schemas.instance import Cgshop2025Instance
from cgshop2025_pyutils.data_schemas.solution import Cgshop2025Solution

import triangle as tr

from solution.our_geometry import *


class RectangleSolver:
    def __init__(self, instance: Cgshop2025Instance):
        self.instance = instance

    def solve(self) -> Cgshop2025Solution:
        points = []
        instance = self.instance
        for x, y in zip(instance.points_x, instance.points_y):
            points.append((x, y))

        rectangles = partition_polygon_to_rectangles(instance.points_x, instance.points_y)
        print("Rectangles:", rectangles)

        plot_partition(x_points, y_points, rectangles)

        # ct.add_boundary(instance.region_boundary)
        # for constraint in instance.additional_constraints:
        #     ct.add_segment(constraint[0], constraint[1])
        #
        boundary_edges = [[self.instance.region_boundary[i],
                           self.instance.region_boundary[(i + 1) % len(self.instance.region_boundary)]] for i in
                          range(len(self.instance.region_boundary))]
        boundary_edges.extend(self.instance.additional_constraints)
        A = dict(vertices=np.array(points), segments=np.array(boundary_edges))
        B = tr.triangulate(A, 'ep')
        tr.compare(plt, A, B)
        plt.show()
        # Extract the triangles (elements)
        triangles = B['triangles'].tolist()  # Each row is a triangle, with 3 vertex indices
        edges = B['edges'].tolist()  # Each row is a triangle, with 3 vertex indices
        # Extract the vertices (original boundary vertices and generated Steiner points)
        steiner_points = B['vertices']

        # Initialize lists for x and y coordinates of Steiner points
        steiner_points_x = []
        steiner_points_y = []

        # Loop through all vertices (exclude boundary vertices to find Steiner points)
        boundary_vertices = set([idx for edge in boundary_edges for idx in edge])

        return Cgshop2025Solution(
            instance_uid=instance.instance_uid,
            steiner_points_x=steiner_points_x,
            steiner_points_y=steiner_points_y,
            edges=edges,
        )
