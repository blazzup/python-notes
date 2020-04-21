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
import pandas as pd
import pandas.util.testing as tu

from uuid import uuid3, NAMESPACE_URL
from pathlib import Path


# %% [markdown]
# # Setup

# %%
def file_name(extension: str) -> str:
    """Create UUID file name from file extension to avoid overwriting existing files."""
    return f'{uuid3(NAMESPACE_URL, extension)}.{extension}'


# %%
tu.N = 5
d = tu.makeDataFrame().set_index('A')
d

# %% [markdown]
# # Export and import


# %% [markdown]
# ## Parquet
#
# Available with pandas $\ge$ 0.21.0

# %%
parquet_file = file_name('parquet')
d.to_parquet(parquet_file)

# %%
pd.read_parquet(parquet_file)

# %% [markdown]
# ### Column names must be strings!

# %%
try:
    d.rename(columns={'B': 1, 'C': 2, 'D': 3}).to_parquet(parquet_file)
except ValueError as e:
    print(e)

# %%
# use .rename(columns=str) for a quick fix
d.rename(columns={'B': 1, 'C': 2, 'D': 3}).rename(columns=str).to_parquet(parquet_file)

# %% [markdown]
# ## Excel
#
# Note: index is stored as an ordinary column!

# %%
excel_file = file_name('xlsx')
d.to_excel(excel_file)

# %%
pd.read_excel(excel_file)

# %%
pd.read_excel(excel_file).set_index('A')  # restore index manually!

# %% [markdown]
# ## Tab-separated txt file with custom float format
#
# Note: index is stored as an ordinary column!

# %%
csv_file = file_name('txt')
d.to_csv(csv_file, sep='\t', float_format='%.2f')

# %%
pd.read_csv(csv_file, sep='\t')

# %%
pd.read_csv(csv_file, sep='\t').set_index('A')  # restore index manually!

# %% [markdown]
# # Benchmark

# %%
tu.N = 100000
d = tu.makeDataFrame()
d.shape

# %% [markdown]
# ## Write

# %%
# %time d.to_parquet(parquet_file)

# %%
# %time d.to_excel(excel_file)

# %%
# %time d.to_csv(csv_file)

# %% [markdown]
# ## Read

# %%
# %time __ = pd.read_parquet(parquet_file)

# %%
# %time __ = pd.read_excel(excel_file)

# %%
# %time __ = pd.read_csv(csv_file)

# %% [markdown]
# ## Size

# %%
pd.DataFrame(
    [(Path(f).suffix, Path(f).stat().st_size) for f in [parquet_file, excel_file, csv_file]],
    columns=['type', 'size'])

# %% [markdown]
# # Remove exported files

# %%
Path(parquet_file).unlink()
Path(excel_file).unlink()
Path(csv_file).unlink()
