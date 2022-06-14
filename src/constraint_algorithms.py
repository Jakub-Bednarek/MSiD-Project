import constraint

from dataset_downloader import DatasetTypes, download_and_convert_all_datasets
from plot_maker import gen_final_plot

DATASETS = download_and_convert_all_datasets()
MIN_SCHOOL_DIST = 950
MAX_SCHOOL_DIST = 1000
MIN_PARK_DIST = 3900
MAX_PARK_DIST = 4000
DIST_X_RANGE = range(
    min(DATASETS[DatasetTypes.Park][0]), max(DATASETS[DatasetTypes.Park][0]), 5000
)
DIST_Y_RANGE = range(
    min(DATASETS[DatasetTypes.Park][1]), max(DATASETS[DatasetTypes.Park][1]), 5000
)


def extract_new_positions(solutions, col1_name, col2_name):
    if not solutions:
        return [], []

    new_xs = []
    new_ys = []
    for sol in solutions:
        new_xs.append(sol[col1_name])
        new_ys.append(sol[col2_name])

    return new_xs, new_ys


def school_dist_constrain(my_x, my_y, school_x, school_y):
    dist_school = (my_x - school_x) ** 2 + (my_y - school_y) ** 2
    if dist_school < MAX_SCHOOL_DIST**2 and dist_school > MIN_SCHOOL_DIST**2:
        return True


def new_park_constrain(new_x, new_y, park_x, park_y):
    dist = (new_x - park_x) ** 2 + (new_y - park_y) ** 2

    if dist > MIN_PARK_DIST**2 and dist < MAX_PARK_DIST**2:
        return True


possible_places_problem = constraint.Problem()
possible_places_problem.addVariable("DIST_X_RANGE", DIST_X_RANGE)
possible_places_problem.addVariable("DIST_Y_RANGE", DIST_Y_RANGE)
possible_places_problem.addVariable("school_lat", DATASETS[DatasetTypes.School][0])
possible_places_problem.addVariable("school_lng", DATASETS[DatasetTypes.School][1])

possible_places_problem.addConstraint(
    school_dist_constrain,
    ["DIST_X_RANGE", "DIST_Y_RANGE", "school_lat", "school_lng"],
)

print("Pos solutions")
solutions = possible_places_problem.getSolutions()

new_xs, new_ys = extract_new_positions(solutions, "DIST_X_RANGE", "DIST_Y_RANGE")

optimal_parks = constraint.Problem()
optimal_parks.addVariable("new_pos_x", new_xs)
optimal_parks.addVariable("new_pos_y", new_ys)
optimal_parks.addVariable("park_x", DATASETS[DatasetTypes.Park][0])
optimal_parks.addVariable("park_y", DATASETS[DatasetTypes.Park][1])
optimal_parks.addConstraint(
    new_park_constrain, ["new_pos_x", "new_pos_y", "park_x", "park_y"]
)

print("Park solutions")
parks_solution = optimal_parks.getSolutions()
extracted_positons = extract_new_positions(parks_solution, "new_pos_x", "new_pos_y")
gen_final_plot(extracted_positons[0], extracted_positons[1])
