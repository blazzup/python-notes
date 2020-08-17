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
# # Base32 encoded JSON
# It can be used to pass JSON strings as command line parameters.  
# If base64 is used instead, it should be verified that `+` and `/` characters will not cause problems in selected shell.  
# **NOTE: On Windows from XP onwards, max. command length is 8191. On Linux systems it should be between 131072 and 2621440.**

# %%
import json, base64

# %%
d = {
    'a': 1,
    'b': 'text',
    'c': [1, 2, 3]
}

# %%
json_string = json.dumps(d)
json_string

# %%
len(json_string)

# %%
e = base64.b32encode(json_string.encode()).decode()
e

# %%
len(e)

# %%
json.loads(base64.b32decode(e))
