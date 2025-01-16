import os.path
import time
import os.path
import time
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
from matplotlib import pyplot as plt

from solution.solvers.rectangle_solver import RectangleSolver
from solution.utils import *

from collections import defaultdict

# Load the instances from the example_instances folder
idb = InstanceDatabase("example_instances/")

# If the solution zip file already exists, delete it
if Path("example_solutions.zip").exists():
    Path("example_solutions.zip").unlink()

# Compute solutions for all instances using the provided (naive) solver
solutions = []
projections = []
for instance in idb:
    # solver = DelaunayBasedSolver(instance)
    # solver = DelaunayCopySolver(instance)
    # solver = OrthogonalSolver(instance)
    solver = RectangleSolver(instance)
    solution = solver.solve()

    # solver = ShirSolver(instance)
    # solution = solver.solve(projections)

    # for i in range(5):
    #     solution = solver.solve(projections)
    #     extra_points = solver.improve_step1(solution)
    #     projections = projections + extra_points
    #     if extra_points==[]:
    #         break
    # core=center_of_mass(extra_points)
    # solution = solver.solve([core])

    # solution2, extra_points = solver.improve_step1(solution)
    # projections=projections + extra_points
    # print("projections")
    # print(projections)
    # solution3 = solver.improve_step2(projections)

    # print("instance:")
    # print(instance)
    # print("solution:")
    # print(solution)
    # solutions.append(solution)
    solutions.append(solution)

# Write the solutions to a new zip file
with ZipWriter("example_solutions.zip") as zw:
    for solution in solutions:
        zw.add_solution(solution)
# Save each plot to a file
output_dir = "output"
Path(output_dir).mkdir(exist_ok=True)

for solution in ZipSolutionIterator("example_solutions.zip"):
    instance = idb[solution.instance_uid]
    result = verify(instance, solution)
    instance_dir = f"{output_dir}/{solution.instance_uid}"
    Path(instance_dir).mkdir(exist_ok=True)
    timestr = time.strftime("%m%d-%H%M%S")
    print(f"{solution.instance_uid}: {result}")
    # assert not result.errors, "Expect no errors."

    # Save solution
    with open(f"{instance_dir}/{timestr}.solution.json", 'w') as f:
        f.write(solution.model_dump_json())

    # Visualize the instance and solution
    # Create a plot
    fig, ax = plt.subplots(figsize=(10, 8))

    points_x = instance.points_x
    points_y = instance.points_y
    # Plot the points
    ax.scatter(points_x, points_y, color='blue')

    new_points_x = [point[0] for point in projections]
    new_points_y = [point[1] for point in projections]
    # print("proj_x")
    # print(proj_x)
    ax.scatter(new_points_x, new_points_y, color='blue', label='Projection Points')

    # Add index labels near each point
    for i, (x, y) in enumerate(zip(points_x, points_y)):
        ax.text(x, y, str(i), fontsize=12, ha='right', color='red')

    # Set axis labels and title
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Instance Plot with Indices")

    # Plot the instance using the provided function
    ax = visualization.plot_instance(ax, instance)

    # Plot the solution on top of the instance
    ax = plot_solution(ax, solution, instance)

    # Finalize plot with legend and show
    ax.legend()
    plt.savefig(f"{instance_dir}/{timestr}.png")

    best_solution_file = f"{instance_dir}/BEST.solution.json"
    best_solution_plot = f"{instance_dir}/BEST.png"
    best_solution = None
    if os.path.isfile(best_solution_file):
        best_solution = read_solution(best_solution_file)

    if is_better_solution(instance, best_solution, result):
        with open(best_solution_file, 'w') as f:
            f.write(solution.model_dump_json())
        plt.savefig(best_solution_plot)

    # Show thew plotted triangles

    plt.show()

    plt.close()