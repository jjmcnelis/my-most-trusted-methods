#!/usr/bin/env python3
import json
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from IPython.display import HTML
tqdm.pandas()

def conf_cmr(url: str="https://cmr.earthdata.nasa.gov", token: str=None):
    headers = {'Echo-Token': token} if token else None
    def collections(ext: str="umm_json", **kwargs):
        kwargs['include_granule_counts'] = "true"
        return requests.get(url=f"{url}/search/collections.{ext}", headers=headers, params=kwargs)
    def granules(ext: str="umm_json", **kwargs):
        return requests.get(url=f"{url}/search/granules.{ext}", headers=headers, params=kwargs)
    return collections, granules

def get_tables(names: list=None, token: str=None):
    coll, gran = conf_cmr(token=token)
    tmp = coll(page_size=2000, provider="POCLOUD").json()
    collections = pd.DataFrame(list(map(lambda x: dict(**x.get("meta"), umm=x.get("umm")), tmp.get("items"))))
    collections['ShortName'] = collections.umm.apply(lambda x: x.get("ShortName"))
    collections['RelatedUrls'] = collections.umm.apply(lambda x: x.get("RelatedUrls"))
    collections['ProcessingLevel'] = collections.umm.apply(lambda x: x.get("ProcessingLevel").get("Id"))
    collections = collections.set_index("ShortName").copy()
    if names:
        collections = collections[collections.index.isin(names)].copy()
    cUrls = pd.concat(collections[~collections.RelatedUrls.isnull()] \
        .apply(lambda x: [{'ShortName': x.name, **u} for u in x['RelatedUrls']], axis=1) \
        .apply(pd.DataFrame) \
        .tolist())
    granules = collections[collections['granule-count']>0] \
        .progress_apply(lambda x: gran(ShortName=x.name, page_size=1).json(), axis=1) \
        .apply(lambda x: x.get("items")[0]) \
        .apply(lambda x: {**x.get("meta"), 'umm': x.get("umm")})
    granules = pd.DataFrame(granules.tolist(), index=granules.index.tolist()).copy()
    granules['RelatedUrls'] = granules.umm.apply(lambda x: x.get("RelatedUrls"))
    gUrls = pd.concat(granules[~granules.RelatedUrls.isnull()] \
        .apply(lambda x: [{'ShortName': x.name, **u} for u in x['RelatedUrls']], axis=1) \
        .apply(pd.DataFrame) \
        .tolist())
    return collections, cUrls, granules, gUrls

def get_urls_common(x, token: str=None):
    ShortName = x.name[1] if len(x.name)==2 else x.name
    return {'web': f"https://podaac.jpl.nasa.gov/dataset/{ShortName}",
            'test': f"https://podaac-test.jpl.nasa.gov/dataset/{ShortName}",
            'mmt': f"https://mmt.earthdata.nasa.gov/collections/{x['concept-id']}",
            'ummc': f"https://cmr.earthdata.nasa.gov/search/collections.umm_json?concept-id={x['concept-id']}&token={token}",
            'ummg': f"https://cmr.earthdata.nasa.gov/search/granules.umm_json?collection_concept_id={x['concept-id']}&token={token}",
            'browse': f"https://cmr.earthdata.nasa.gov/virtual-directory/collections/{x['concept-id']}",
            'search': f"https://search.earthdata.nasa.gov/search/granules?p={x['concept-id']}", }

def get_html(x):
    return {k: f'<a href="{v}">{k}</a>' for k,v in x.items() if v.startswith("http")}
