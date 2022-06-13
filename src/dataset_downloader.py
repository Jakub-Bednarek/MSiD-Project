import dotenv
import pandas as pd

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
    

def download_all_datasets():
    return {
        DatasetTypes.Business: download_single_dataset(DEFAULT_BUSINNES_LOCATIONS_API_ENDPOINT, BUSINESS_LOCATIONS_COLUMNS),
        DatasetTypes.School: download_single_dataset(DEFAULT_SCHOOL_API_ENDPOINT, SCHOOL_COLUMNS),
        DatasetTypes.Park: download_single_dataset(DEFAULT_PARK_API_ENDPOINT, PARK_COLUMNS)
    }