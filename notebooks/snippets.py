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
# ### Use SVG format for displaying plots inside notebook (better image quality)

# %%
# %config InlineBackend.figure_format = 'svg'

# %% [markdown]
# ### Switch to interactive mode (opens separate window)

# %%
# %matplotlib qt

# %% [markdown]
# ### Load and use line profiler
#
# Requirements: `conda install line_profiler`

# %%
# %load_ext line_profiler

# %%
# %lprun -f function_to_profile function_to_call()

# %% [markdown]
# ### Switch to inline mode (closes the interactive figure!)

# %%
# %matplotlib inline

# %% [markdown]
# ### Generate test data frames

# %%
import pandas as pd
import pandas.util.testing as tu

# %%
pd.np.random.seed(0)
tu.N = 3
tu.K = 5
tu.makeDataFrame()

# %% [markdown]
# ### Show all rows or columns

# %%
pd.options.display.expand_frame_repr = False

# the following lines are needed if dataframe actually contains more rows or columns
pd.options.display.max_rows = 0
pd.options.display.max_columns = 0

# %% [markdown]
# ### Restart current kernel without dialog

# %%
from IPython.core.display import HTML

HTML("<script>Jupyter.notebook.kernel.restart()</script>")
