from dataset_downloader import (
    DatasetTypes,
    MAX_DECIMAL_PLACES,
    download_all_datasets,
    convert_polygons_to_x_y_pos_df,
    convert_points_to_x_y_pos_df,
)

import matplotlib.pyplot as plt
import pandas as pd

PLOT_FOLDER = "images/plots"
DATASETS = download_all_datasets()
PARK_X_LIM = (37.7, 37.83)
PARK_Y_LIM = (-122.525, -122.375)
BUSINESS_X_LIM = (37.2, 38.4)
BUSINESS_Y_LIM = (-122.75, -121.5)


def save_parks_plot():
    converted_df = convert_polygons_to_x_y_pos_df(DATASETS[DatasetTypes.Park])

    converted_df.plot(x="Latitude", y="Longitude", kind="scatter", s=40)
    plt.xlim(PARK_X_LIM[0], PARK_X_LIM[1])
    plt.ylim(PARK_Y_LIM[0], PARK_Y_LIM[1])
    plt.savefig(f"{PLOT_FOLDER}/parks.png")


def save_business_plot():
    converted_df = convert_points_to_x_y_pos_df(
        DATASETS[DatasetTypes.Business], "location", "POINT ", " ", True
    )
    converted_df.plot(x="Latitude", y="Longitude", kind="scatter", s=40)
    plt.xlim(BUSINESS_X_LIM[0], BUSINESS_X_LIM[1])
    plt.ylim(BUSINESS_Y_LIM[0], BUSINESS_Y_LIM[1])
    plt.savefig(f"{PLOT_FOLDER}/business.png")


def save_school_plot():
    converted_df = convert_points_to_x_y_pos_df(
        DATASETS[DatasetTypes.School], "location_1", "\n, CA \n"
    )
    converted_df.plot(x="Latitude", y="Longitude", kind="scatter", s=40)
    plt.savefig(f"{PLOT_FOLDER}/school.png")


def convert_x_and_y(x_list, y_list):
    new_x = []
    new_y = []

    for i in range(0, len(x_list)):
        new_x.append(float(x_list[i]) / MAX_DECIMAL_PLACES)
        new_y.append(float(y_list[i]) / MAX_DECIMAL_PLACES)

    return new_x, new_y


def gen_final_plot(x_list, y_list):
    new_x, new_y = convert_x_and_y(x_list, y_list)

    plt.scatter(new_x, new_y, s=40, color=[0.3, 0.5, 0.8, 0.1])
    plt.xlim(PARK_X_LIM[0], PARK_X_LIM[1])
    plt.ylim(PARK_Y_LIM[0], PARK_Y_LIM[1])
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
    plt.title(label="Optymalne miejsca dla parków")
    plt.savefig(f"{PLOT_FOLDER}/optimal_parks.png")
    plt.show()


def save_all_plots():
    save_parks_plot()
    save_business_plot()
    save_school_plot()


# save_all_plots()
