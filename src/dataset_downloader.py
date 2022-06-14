import dotenv
import pandas as pd
import shapely.wkt

from typing import List
from enum import Enum, auto

dotenv.load_dotenv()

DEFAULT_BUSINNES_LOCATIONS_API_ENDPOINT = "https://data.sfgov.org/resource/g8m3-pdis.csv"
BUSINESS_LOCATIONS_COLUMNS = ['location']
DEFAULT_SCHOOL_API_ENDPOINT = "https://data.sfgov.org/resource/tpp3-epx2.csv"
SCHOOL_COLUMNS = ['location_1']
DEFAULT_PARK_API_ENDPOINT = "https://data.sfgov.org/resource/gtr9-ntp6.csv"
PARK_COLUMNS = ['shape']

class DatasetTypes(Enum):
    Business = auto()
    School = auto()
    Park = auto()
    

def download_single_dataset(api_endpoint: str, columns_to_select: List = None):
    df = pd.read_csv(api_endpoint)

    if columns_to_select:
        return df[columns_to_select]
    else:
        return df
    
def convert_polygons_to_x_y_pos(dataset):
    df = pd.DataFrame({'Latitude': [], 'Longitude': []})
    
    for poly in dataset['shape']:
        y_list, x_list = (shapely.wkt.loads(poly).convex_hull.exterior.coords.xy)
        x_sum = sum(x_list)
        y_sum = sum(y_list)
        df.loc[len(df.index)] = [x_sum / len(x_list), y_sum / len(y_list)]
        
    return df

def convert_points_to_x_y_pos(dataset, column_name: str, prefix_to_remove: str = None, delimiter: str =',', swap_x_y=False):
    x, y = [], []
    for point in dataset[column_name]:
        if point != None:
            no_prefix = point[len(prefix_to_remove) + 1:-1]
            splitted = no_prefix.split(delimiter)
            x.append(float(splitted[0]))
            y.append(float(splitted[1]))
        
    if swap_x_y:
        return pd.DataFrame({'Latitude': y, 'Longitude': x})
    
    return pd.DataFrame({'Latitude': x, 'Longitude': y})
    

def download_all_datasets():
    return {
        DatasetTypes.Business: download_single_dataset(DEFAULT_BUSINNES_LOCATIONS_API_ENDPOINT, BUSINESS_LOCATIONS_COLUMNS),
        DatasetTypes.School: download_single_dataset(DEFAULT_SCHOOL_API_ENDPOINT, SCHOOL_COLUMNS),
        DatasetTypes.Park: download_single_dataset(DEFAULT_PARK_API_ENDPOINT, PARK_COLUMNS)
    }