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

from datetime import datetime, timedelta

# %% [markdown]
# ## Timestamp

# %% [markdown]
# ### pandas.Timestamp inherits from datetime.datetime

# %%
t1 = pd.Timestamp(datetime(2020, 1, 1))
t1

# %%
isinstance(t1, pd.Timestamp)

# %%
isinstance(t1, datetime)

# %% [markdown]
# ### convert to datetime.datetime

# %%
t2 = pd.Timestamp('2020').to_pydatetime()
t2

# %%
isinstance(t2, pd.Timestamp)

# %%
isinstance(t2, datetime)

# %% [markdown]
# ## Timedelta

# %% [markdown]
# ### pandas.Timedelta inherits from datetime.timedelta

# %%
dt = pd.Timedelta(1, unit='s')
dt

# %%
isinstance(dt, timedelta)

# %%
timedelta(seconds=1) + dt

# %%
datetime(2020, 1, 1) + dt

# %% [markdown]
# ## Timezone

# %%
t = pd.Timestamp('2020-1-1 12:00:00')

# %% [markdown]
# ### Add or remove timezone (tz_localize)

# %%
t.tz_localize('UTC')  # add timezone, do not change value

# %%
try:
    t.tz_localize('UTC').tz_localize('CET')  # timezone change not possible with tz-aware timestamp
except TypeError as e:
    print(e)

# %%
t.tz_localize('UTC').tz_localize(None).tz_localize('CET')

# %% [markdown]
# ### Convert time (astimezone)
# Use this to keep the same time: 12:00 UTC -> 13:00 CET

# %%
t.tz_localize('UTC').astimezone('CET')  # conversion between different times

# %% [markdown]
# ## DateTimeIndex

# %%
pd.np.random.seed(0)
tu.N = 5
tu.K = 2
d = tu.makeTimeDataFrame(freq='s')
d

# %%
d.index

# %% [markdown]
# ### Index to seconds

# %%
idx = (d.index - d.index[0]) / pd.Timedelta('1s')
idx

# %% [markdown]
# ### Seconds to index

# %%
pd.TimedeltaIndex(idx, unit='s') + pd.Timestamp('2000-1-1')

# %% [markdown]
# ## Unix time
# Note: due to leap seconds, unix time is not a true representation of UTC. 

# %%
# seconds to timestamp
time = pd.to_datetime(60, unit='s', origin='unix', utc=True)
time

# %%
# timestamp to seconds
seconds = (time - pd.to_datetime(0, unit='s', origin='unix', utc=True)).total_seconds()
seconds
