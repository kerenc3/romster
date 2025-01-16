from fractions import Fraction
import functools
from pathlib import Path

from cgshop2025_pyutils import (
    DelaunayBasedSolver,
    InstanceDatabase,
    ZipSolutionIterator,
    ZipWriter,
    verify,
    visualization,
    VerificationResult
)

from cgshop2025_pyutils.data_schemas.instance import Cgshop2025Instance
from cgshop2025_pyutils.data_schemas.solution import Cgshop2025Solution

def plot_solution(ax, solution, instance):
    """Plot the solution including Steiner points and edges."""
    # Convert Steiner points' x and y coordinates
    steiner_points_x = [
        float(Fraction(x)) if isinstance(x, str) else x for x in solution.steiner_points_x
    ]
    steiner_points_y = [
        float(Fraction(y)) if isinstance(y, str) else y for y in solution.steiner_points_y
    ]

    # Plot the instance points
    visualization.plot_instance(ax, instance)

    # Plot Steiner points
    ax.scatter(steiner_points_x, steiner_points_y, color="green", label="Steiner Points")

    # Plot edges
    all_points_x = instance.points_x + steiner_points_x
    all_points_y = instance.points_y + steiner_points_y
    for edge in solution.edges:
        x1, y1 = all_points_x[edge[0]], all_points_y[edge[0]]
        x2, y2 = all_points_x[edge[1]], all_points_y[edge[1]]
        ax.plot([x1, x2], [y1, y2], color="orange", linestyle="-", linewidth=1)

    ax.legend()
    ax.set_title(f"Solution: {instance.instance_uid}")
    return ax


def is_better_solution(instance: Cgshop2025Instance, best: Cgshop2025Solution, potential: VerificationResult) -> bool:
    if best == None:
        return True

    best_result = verify(instance, best)
    if len(potential.errors) > len(best_result.errors):
        print("more errors")
        return False
    if len(potential.errors) == 0 and len(best_result.errors) > 0:
        return True
    if potential.num_obtuse_triangles > best_result.num_obtuse_triangles:
        print("more triangles")
        return False
    if best_result.num_obtuse_triangles == 0 and potential.num_steiner_points > best_result.num_steiner_points:
        print("more romsters")
        return False
    return True


def open_file(func):
    """
    Decorator to open a file before calling the function and close it afterwards,
    if passed as string or pathlib.Path.
    """

    @functools.wraps(func)
    def wrapper(file, *args, **kwargs):
        if isinstance(file, str):
            file = Path(file)
        if isinstance(file, Path):
            with file.open() as f:
                return func(f, *args, **kwargs)
        return func(file, *args, **kwargs)

    return wrapper

@open_file
def read_solution(file) -> Cgshop2025Solution:
    """
    Read a solution from a file.
    :param file: File object or path to the file.
    :return: Solution object
    """
    content = file.read()
    return Cgshop2025Solution.model_validate_json(content)