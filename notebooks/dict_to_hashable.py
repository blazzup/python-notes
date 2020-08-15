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

# %% [markdown]
# # Test data

# %%
a_dict = {'aaa10': 1, 'aaa4': 2, 'aaa2': 3, 'aaa8': 3.14, 'aaa1': '5', 'aaa7': True}
a_dict

# %% [markdown]
# ### To frozenset

# %%
a_set = frozenset(a_dict.items())
a_set

# %% [markdown]
# ### To sorted tuple

# %%
a_tuple = sorted(tuple(a_dict.items()))
a_tuple

# %% [markdown]
# ### To string

# %%
a_string = json.dumps(a_dict, sort_keys=True)
a_string

# %% [markdown]
# ### Back to dict

# %%
dict(a_set)

# %%
dict(a_tuple)

# %%
json.loads(a_string)

# %% [markdown]
# # Benchmark

# %% [markdown]
# ### From dict

# %%
# %timeit frozenset(a_dict.items())

# %%
# %timeit sorted(tuple(a_dict.items()))

# %%
# %timeit json.dumps(a_dict, sort_keys=True)

# %% [markdown]
# ### To dict

# %%
# %timeit dict(a_set)

# %%
# %timeit dict(a_tuple)

# %%
# %timeit json.loads(a_string)

# %% [markdown]
# ### Comparison

# %%
a = frozenset(a_dict.items())
a2 = frozenset(a_dict.items())

# %%
b = sorted(tuple(a_dict.items()))
b2 = sorted(tuple(a_dict.items()))

# %%
c = json.dumps(a_dict, sort_keys=True)
c2 = json.dumps(a_dict, sort_keys=True)

# %%
# %timeit a==a2

# %%
# %timeit b==b2

# %%
# %timeit c==c2
