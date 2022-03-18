from concurrent.futures import ThreadPoolExecutor
import requests
import os.path

def modularize(module_file: str, module_name: str):
    initf = os.path.join(module_file, module_name, '__init__.py')
    if not os.path.exists(initf):
        open(initf, 'wb').close()
  
def import_stats():
    for k,v in globals().items():
        if 'module' in str(type(v)):
            if hasattr(v, "__path__"):
                print(f"  {v.__name__}  \t{v.__version__ }\t({v.__path__[0]})")

def download_file(url: str, target: str, force: bool=False):
    if not os.path.isfile(target) or force is True:
        with requests.get(url) as response, open(target, 'wb') as file:
            if not response.status_code // 100 == 2: 
                raise Exception(response.text)
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
    return target

def download_pool(jobs: list, max_workers: int=12) -> list:
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(tqdm(pool.map(lambda x: download_file(*x), jobs), total=len(jobs)))
