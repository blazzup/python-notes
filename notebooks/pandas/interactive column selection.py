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
import easygui
import pandas as pd
import pandas.util.testing as tu

# %% [markdown]
# ## Basic easygui functionality
#
# Note: the development of this module does not seem to be very active,
# but it does offer an extremely easy to use interface.

# %%
selected = easygui.multchoicebox(msg='Select columns', choices=['a', 'b'])
print(selected)


# %% [markdown]
# ## Select data frame columns and preserve selection
#
# This is meant for interactive work only and makes use of global variable 'column_list'.

# %%
def select_columns(data):
    def ok_button_click(choice_box):
        """Return empty list instead of None when OK is pressed and nothing was selected."""
        if choice_box.choices is None:
            choice_box.choices = []
        choice_box.stop()

    global column_list

    # create global variable if not present yet
    if 'column_list' not in globals():
        column_list = []

    # reset selection if not all names are found in data columns
    if set(data.columns) & set(column_list) != set(column_list):
        column_list = []

    new_selection = easygui.multchoicebox(
        msg='Select columns',
        choices=data.columns,
        preselect=list(map(data.columns.get_loc, column_list)),  # preselect takes index, not name
        callback=ok_button_click,
    )
    column_list = new_selection if new_selection is not None else column_list


# %%
pd.np.random.seed(0)
tu.N = 3
tu.K = 10
d = tu.makeDataFrame()
d

# %%
select_columns(d)
d[column_list]
