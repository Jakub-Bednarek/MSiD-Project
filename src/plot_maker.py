from lib2to3.pytree import convert
from numpy import save
from dataset_downloader import download_all_datasets, DatasetTypes, convert_polygons_to_x_y_pos, convert_points_to_x_y_pos

import matplotlib.pyplot as plt
import pandas as pd

PLOT_FOLDER = "images/plots"
DATASETS = download_all_datasets()
PARK_X_LIM = (37.65, 37.83)
PARK_Y_LIM = (-122.55, -122.35)
BUSINESS_X_LIM = (37.2, 38.4)
BUSINESS_Y_LIM = (-122.75, -121.5)

def save_parks_plot():
    converted_df = convert_polygons_to_x_y_pos(DATASETS[DatasetTypes.Park])
    
    converted_df.plot(x='Latitude', y='Longitude', kind='scatter', s=40)
    plt.xlim(PARK_X_LIM[0], PARK_X_LIM[1])
    plt.ylim(PARK_Y_LIM[0], PARK_Y_LIM[1])
    plt.savefig(f"{PLOT_FOLDER}/parks.png")
    
    
def save_business_plot():
    converted_df = convert_points_to_x_y_pos(DATASETS[DatasetTypes.Business], 'location', 'POINT ', ' ', True)
    converted_df.plot(x='Latitude', y='Longitude', kind='scatter', s=40)
    plt.xlim(BUSINESS_X_LIM[0], BUSINESS_X_LIM[1])
    plt.ylim(BUSINESS_Y_LIM[0], BUSINESS_Y_LIM[1])
    plt.savefig(f"{PLOT_FOLDER}/business.png")
    

def save_school_plot():
    converted_df = convert_points_to_x_y_pos(DATASETS[DatasetTypes.School], "location_1", '\n, CA \n')
    converted_df.plot(x='Latitude', y='Longitude', kind='scatter', s=40)
    plt.savefig(f"{PLOT_FOLDER}/school.png")

def save_all_plots():
    save_parks_plot()
    save_business_plot()
    save_school_plot()

save_all_plots()