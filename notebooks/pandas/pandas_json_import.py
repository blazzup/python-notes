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
import json

import pandas as pd
from pandas.io.json import json_normalize

# %% [markdown]
# ## Test data

# %%
d0 = {'int': 42, 'string': 'answer', 'float': 3.14, 'list': [10, 20, 30]}
d0

# %%
d = {
    'dict': {'a': 1, 'b': 2},
    'list_of_dict': [{'a': 1, 'b': 2, 'dict': {'a': 3, 'b': 4}},
                     {'a': 5, 'b': 6, 'dict': {'a': 7, 'b': 8}}],
}
d.update(d0)
d

# %%
json.dumps(d0)

# %%
json.dumps(d)

# %% [markdown]
# ## Built-in `read_json()`
#
# Can expand lists into multiple rows, but does not work with more complicated dicts.  
# The expected structure is set by orient parameter.

# %%
pd.read_json(json.dumps(d0))

# %%
pd.read_json(json.dumps(d0), orient='index')

# %%
orient = ['split', 'records', 'index', 'columns', 'values', 'table']
for o in orient:
    try:
        pd.read_json(json.dumps(d), orient=o)
    except Exception as exc:
        print(exc)

# %% [markdown]
# ### Import list of records
#
# No flattening of dictionaries and no expanding of lists!

# %%
pd.read_json(json.dumps([d0]))

# %%
pd.read_json(json.dumps([d]))

# %% [markdown]
# ## Built-in `json_normalize()`
#
# Expands dicts, but not lists.

# %%
json_normalize(d0)

# %%
json_normalize(d)

# %% [markdown]
# ## Manual flattening

# %%
df = pd.DataFrame([d] * 3)
df

# %% [markdown]
# ### Select columns by type

# %%
df.iloc[0].apply(type)

# %%
df.iloc[0].apply(type) == list

# %% [markdown]
# ### Flatten dicts

# %%
df['dict']

# %%
pd.DataFrame(df['dict'].tolist())

# %% [markdown]
# ### Flatten lists

# %%
df['list']

# %%
pd.DataFrame(df['list'].apply(enumerate).apply(dict).tolist())


# %% [markdown]
# ### Final solution
#
# - iteratively flatten all lists and all dicts
# - exclude specified columns from default processing and use custom functions istead

# %%
def _expand_column(data: pd.DataFrame, name: str, func, custom_columns: dict, sep: str) -> pd.DataFrame:
    """Split a single column into one or more columns by applying func."""
    new_columns = pd.DataFrame(func(data[name]))

    # prefix column names with parent name
    name_map = {current_name: f'{name}{sep}{current_name}' for current_name in new_columns.columns}

    # add new names to custom columns dict so that they will be processed correctly
    for current_name in set(new_columns.columns) & set(custom_columns):
        new_name = name_map[current_name]
        custom_columns[new_name] = custom_columns[current_name]  # map to the same processing function

    new_columns.rename(name_map, axis=1, inplace=True)

    return new_columns


def expand(data: pd.DataFrame, custom_columns: dict = None, sep: str = '_', depth=100) -> pd.DataFrame:
    """Expand list and dict columns in pandas data frame.

    Args:
        data: Input data frame.
        custom_columns: Dictionary of column names which should be excluded from default processing
            and use custom functions instead.
        sep: Separator to use when merging parent and child names.
        depth: Maximum number of hierarchy levels to expand.
    """
    if data.empty:
        return data

    if custom_columns is None:
        custom_columns = {}

    # expand lists and dicts
    for i in range(depth):
        first_row = data.iloc[0]  # creates a series with column names as index
        column_type = first_row.apply(type)

        list_columns = set(first_row.index[column_type == list]) - set(custom_columns)
        dict_columns = set(first_row.index[column_type == dict]) - set(custom_columns)
        if not list_columns and not dict_columns:
            break
        if i + 1 == depth:
            raise RuntimeError((f'Number of hierarchy levels exceeded, '
                                f'increase depth parameter (currently depth={depth})'))

        new_columns = []
        for name in list_columns:
            new_columns.append(
                _expand_column(data, name,
                               lambda column: column.apply(lambda item: dict(enumerate(item))).tolist(),
                               custom_columns, sep)
            )
        for name in dict_columns:
            new_columns.append(
                _expand_column(data, name, lambda column: column.tolist(), custom_columns, sep)
            )

        remaining_columns = data[set(data.columns) - (list_columns | dict_columns)]
        new_columns.append(remaining_columns)
        data = pd.concat(new_columns, axis=1)

    # process custom columns
    for name, func in custom_columns.items():
        if name in data.columns:
            data[name] = data[name].apply(func)

    return data


# %%
expand(df)

# %%
expand(df, custom_columns={'dict': str})

# %% [markdown]
# ### Benchmark

# %%
# %%timeit
expand(pd.DataFrame([d]), custom_columns={'dict': str})

# %%
# %%timeit
expand(pd.DataFrame([d] * 10000), custom_columns={'dict': str})
