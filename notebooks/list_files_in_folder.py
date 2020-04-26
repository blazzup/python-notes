# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import re

from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime
from pprint import pprint


# %% [markdown]
# ## Setup

# %%
def run_example(function):
    """Setup test files and run user function with folder passed in as the parameter."""
    with TemporaryDirectory() as folder:
        subfolder = Path(folder, 'sub')
        subfolder.mkdir()
        for i in range(3):
            Path(folder, f'test-{i:03d}.txt').touch()
            Path(subfolder, f'file-{i:03d}.txt').touch()
        Path(subfolder, f'file-xyz.txt').write_text('hello')

        pprint(function(folder))  # function for listing contents


# %% [markdown]
# ## List files

# %%
def list_all(folder):
    file_list = Path(folder).glob('**/*.txt')
    return list(map(str, file_list))


run_example(list_all)


# %%
def list_numeric(folder):
    file_list = Path(folder).glob('**/file*.txt')

    file_index = []
    p = re.compile('-(\d+)\.')  # search for number with leading "-" and trailing "."
    for file in file_list:
        m = p.search(str(file))
        idx = int(m.group(1)) if m is not None else float('nan')
        file_index.append({
            'idx': idx,
            'name': file.name,
            'size': file.stat().st_size,
            'last_update': datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
        })
        # output can be used directly with pandas, e.g.:
        # pd.DataFrame(file_index).dropna().set_index('idx').sort_index()

    return file_index


run_example(list_numeric)

