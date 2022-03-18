# ipynb/

Basic usage of any script from [py/](https://github.com/jjmcnelis/trusted-methods/tree/main/py) directory:

```python
def import_from_github(url: str):
    import imp
    with requests.get(url) as response: 
        module = imp.new_module("swot")
        exec(response.text, module.__dict__)
        return module

cmn = import_from_github("https://raw.githubusercontent.com/jjmcnelis/trusted-methods/main/py/cmn.py")
```

Then, invoke the function `download` like so:

```python
cmn.download("https://example.com/file.txt")
```

**Selected examples:**

* [swot_nadir_example.ipynb](swot_nadir_example.ipynb)
