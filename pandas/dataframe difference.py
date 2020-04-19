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

# %% [markdown]
# ## Setup
#
# Multiindex is used to highlight specific behavior.

# %%
d1 = pd.DataFrame({
    'a': [1, 1, 3],
    'b': [11, 22, 22],
    'c': [4, 9, 9],
    'd': [5, 4, 3]}
).set_index(['a', 'b', 'c'])
d1

# %%
d2 = d1.copy()
d2.loc[(1, 22, 8), :] = 4
d2 = d2.drop((1, 22, 9)).sort_index()
d2

# %% [markdown]
# ## Quickly show distinct items
#
# Removes all rows which are found in both dataframes, set equivalent of: (a | b) - (a & b)  

# %%
# drop_duplicates() does not take index into account!!!
pd.concat([d1, d2]).drop_duplicates(keep=False)

# %%
pd.concat([d1.reset_index(), d2.reset_index()]).drop_duplicates(keep=False)

# %% [markdown]
# ## Set difference on index

# %%
pd.DataFrame(
    index=d1.index.difference(d2.index)
)

# %%
pd.DataFrame(
    index=d2.index.difference(d1.index)
)

# %% [markdown]
# ## Test for equality

# %%
try:
    tu.assert_frame_equal(d1, d2)
    print('Data frames are the same.')
except AssertionError as err:
    print(err)

# %%
try:
    tu.assert_frame_equal(d1, d1.copy())
    print('Data frames are the same.')
except AssertionError as err:
    print(err)
