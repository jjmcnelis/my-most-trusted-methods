import os
import requests
import pandas as pd
import xarray as xr
import shapely.geometry as geom
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime as dt
from io import StringIO
from tqdm import tqdm
tqdm.pandas()

def download(source: str):
    target = os.path.join(data, os.path.basename(source.split("?")[0]))
    if not os.path.isfile(target):
        !wget --quiet --continue --output-document $target $source
    return target

def download_all(urls: list, max_workers: int=12):
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        workers = pool.map(download, urls)
        return list(tqdm(workers, total=len(urls)))

def swot_granule_query_example(ccid: str, cmr: str="cmr.earthdata.nasa.gov", **kwargs):
    GranuleUR = {
        'cycle':      "???",         # 3 digit cycle
        'pass':       "???",         # 3 digit pass
        'start_date': "????????",    # 8 digit date (yyyymmdd),
        'start_time': "??????",      # 6 digit date (hhmmss),
        'end_date':   "????????",    # 8 digit date (yyyymmdd),
        'end_time':   "??????",      # 6 digit date (hhmmss)
    }
    
    # Merge the input keyword arguments to configure the GranuleUR query string
    pattern = {**GranuleUR, **{k:(str(v).zfill(3) if type(v) is int else v) for k,v in kwargs.items()}}
    
    # Format the 'GranuleUR' string to complete the parameters dictionary
    params = {
        'scroll': "true",
        'page_size': 2000,
        'collection_concept_id': ccid,
        'GranuleUR[]': "SWOT_GPR_2PTP{cycle}_{pass}_{start_date}_{start_time}_{end_date}_{end_time}".format(**pattern),
        'options[GranuleUR][pattern]': "true",
    }
    
    # Download the granule metadata in csv format and load the records into a data frame
    with requests.get(f"https://{cmr}/search/granules.csv", params=params) as response:
        metadata = pd.read_csv(StringIO(response.text))
    
    return metadata
