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

from solution.solvers.orthogonal_solver import OrthogonalSolver
from solution.utils import *

# Load the instances from the example_instances folder
idb = InstanceDatabase("try/")

# If the solution zip file already exists, delete it
if Path("example_solutions.zip").exists():
    Path("example_solutions.zip").unlink()

# Compute solutions for all instances using the provided (naive) solver
solutions = []
print("fdjfd")

for instance in idb:
    solver = OrthogonalSolver(instance)
    solution = solver.solve()
    solutions.append(solution)

# Write the solutions to a new zip file
with ZipWriter("example_solutions.zip") as zw:
    for solution in solutions:
        zw.add_solution(solution)
# Save each plot to a file
output_dir = "output"
Path(output_dir).mkdir(exist_ok=True)
print("fdjfd2")

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


    plt.show()

    plt.close()