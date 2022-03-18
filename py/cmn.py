import os
import sys
import json
import hashlib
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def file_hash(file: str, blocksize=4096):
    """Return hex digest for the input `file` in chunks of `blocksize`"""
    sha = hashlib.sha256()
    with open(file, 'rb') as fp:
        while 1:
            data = fp.read(blocksize)
            if data:
                sha.update(data)
            else:
                break
    return sha.hexdigest()

def file_stat(file: str, mult: float=0.001, tfmt: str="%Y-%m-%d %H:%M:%S"):
    stat = os.stat(file)
    return {"name": os.path.basename(file), 
            "size": stat.st_size * mult, 
            "date": datetime.fromtimestamp(stat.st_mtime).strftime(tfmt), }

def file_import(module_file: str, module_name: str):
    initf = os.path.join(module_file, module_name, '__init__.py')
    if not os.path.exists(initf):
        open(initf, 'wb').close()

def list_imports():
    _imports = []
    for k,v in globals().items():
        if 'module' in str(type(v)):
            if hasattr(v, "__path__"):
                _imports.append((v.__name__,v.__version__,v.__path__[0]))
    return _imports

def walk_directory(path: str, extn: str=None, skip: list=None) -> list:
    _files = []
    for root, dirs, files in os.walk(path):
        for f in files:
            fext = os.path.splitext(f)[1]
            if extn is None or extn in fext:
                if skip is None or fext not in skip:
                    _files.append(os.path.join(root, f))
    return _files

def download(url: str, target: str=None, force: bool=False, chunk_size: int=1024) -> str:
    if target is None:
        target = os.path.join(data, os.path.basename(source.split("?")[0]))
    if not os.path.isfile(target) or force is True:
        with requests.get(url, stream=True) as response, open(target, 'wb') as file:
            if response.status_code // 100 == 2: 
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
    return target

def download_all(urls: list, max_workers: int=12) -> list:
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(tqdm(pool.map(lambda x: download(*x), urls), total=len(urls)))
