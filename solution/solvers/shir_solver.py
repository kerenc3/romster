from cgshop2025_pyutils.data_schemas.instance import Cgshop2025Instance
from cgshop2025_pyutils.data_schemas.solution import Cgshop2025Solution
import numpy as np
from scipy.spatial import Delaunay

# from ..geometry import ConstrainedTriangulation, Point


class ShirSolver:
    def __init__(self, instance: Cgshop2025Instance):
        self.instance = instance

    def solve(self) -> Cgshop2025Solution:
        ct = ConstrainedTriangulation()
        instance = self.instance
        points = np.array([[x, y] for x, y in zip(instance.points_x, instance.points_y)])
        tri = Delaunay(points)
        #     ct.add_point(Point(x, y))
        # ct.add_boundary(instance.region_boundary)
        # for constraint in instance.additional_constraints:
        #     ct.add_segment(constraint[0], constraint[1])
        # edges = ct.get_triangulation_edges()
        # return Cgshop2025Solution(
        #     instance_uid=instance.instance_uid,
        #     steiner_points_x=[],
        #     steiner_points_y=[],
        #     edges=edges,
        # )
        # import matplotlib.pyplot as plt
        plt.triplot(points[:,0], points[:,1], tri.simplices)
        plt.plot(points[:,0], points[:,1], 'o')
        plt.show()


# points = np.array([[0, 0], [0, 1.1], [1, 0], [1, 1]])
# from scipy.spatial import Delaunay
# tri = Delaunay(points)