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

# %% [markdown]
# ## Remove from list

# %% [markdown]
# ### Use [:] to change existing list

# %%
a = [1, 2, 3]
id(a), a

# %%
a[:] = [x for x in a if x < 3]
id(a), a

# %% [markdown]
# ### Normal assignment creates a new list

# %%
a = [1, 2, 3]
id(a), a

# %%
a = [x for x in a if x < 3]
id(a), a

# %% [markdown]
# ## Remove from set

# %% [markdown]
# ### Use intersection update

# %%
a = {1, 2, 3}
id(a), a

# %%
a &= {x for x in a if x < 3}
# a.intersection_update({x for x in a if x < 3})  # long version
id(a), a

# %% [markdown]
# ### Normal intersection creates a new set

# %%
a = {1, 2, 3}
id(a), a

# %%
a = a & {x for x in a if x < 3}
id(a), a

# %% [markdown]
# ## Remove from dict

# %% [markdown]
# ### Use del to manually remove keys

# %%
a = {'a': 1, 'b': 2, 'c': 3}
id(a), a

# %%
to_remove = [k for k, v in a.items() if not v < 3]
for k in to_remove:
    del a[k]
id(a), a

# %% [markdown]
# ### Alternative: clear and update

# %%
a = {'a': 1, 'b': 2, 'c': 3}
id(a), a

# %%
new_dict = {k: v for k, v in a.items() if v < 3}
a.clear()
a.update(new_dict)
id(a), a

# %% [markdown]
# ### Normal assignment creates a new dict

# %%
a = {'a': 1, 'b': 2, 'c': 3}
id(a), a

# %%
a = {k: v for k, v in a.items() if v < 3}
id(a), a

# %% [markdown]
# ## Remove from tuple

# %%
a = (1, 2, 3)
id(a), a

# %% [markdown]
# ### Tuples are immutable!

# %%
try:
    a[:] = tuple(x for x in a if x < 3)
    id(a), a
except TypeError as exc:
    print(exc)

# %% [markdown]
# ### New tuple must be created

# %%
a = tuple(x for x in a if x < 3)
id(a), a
