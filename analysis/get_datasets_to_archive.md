```python
import pandas as pd
import jupyter_black
from datetime import datetime

jupyter_black.load()
```

```python
# URL of dataset CSV. Be sure to regenerate for the
# current year before running.
DATASET_INFO_CSV = (
    "https://raw.githubusercontent.com/OCHA-DAP/"
    + "hdx-analysis-scripts/gh-pages/datasets_info/datasets.csv"
)
# We only want to consider datasets 5 years or older
# e.g. In January 2022, we archived datasets created
# before 31 December 2016. UPPER_BOUND_YEAR should
# be used with an exclusive < (i.e. dataset years < UPPER_BOUND_YEAR)
UPPER_BOUND_YEAR = datetime.today().year - 5
# Max number of downloads in the past 5 years
MAX_DOWNLOADS = 1_000
```

```python
UPPER_BOUND_YEAR
```

```python
# Takes awhile to read in because it's a large file
df = pd.read_csv(DATASET_INFO_CSV)
```

```python
# The number of rows
df.shape[0]
```

```python
# Let's look at the column names
df.columns
```

```python
# We don't want datasets that are already archived
df_noarchive = df.loc[df["archived"] == "N"]
df_noarchive.shape[0]
```

```python
# We only want to consider datasets that were created more than 5 years ago
df_noarchive_5yo = df_noarchive.loc[
    pd.to_datetime(df_noarchive["date created"]).dt.year < UPPER_BOUND_YEAR
]
df_noarchive_5yo.shape[0]
```

```python
# Confirm maximum date is < UPPER_BOUND_YEAR
df_noarchive_5yo["date created"].max()
```

```python
# Datasets must have < 1000 download counts
df_noarchive_5yo_lt1000dl = df_noarchive_5yo.loc[
    df_noarchive_5yo["downloads last 5 years"] < MAX_DOWNLOADS
]
df_noarchive_5yo_lt1000dl.shape[0]
```

```python
# Datasets must not be CODs
df_noarchive_5yo_lt1000dl_notcod = df_noarchive_5yo_lt1000dl.loc[
    df_noarchive_5yo_lt1000dl["is cod"] == "N"
]
df_noarchive_5yo_lt1000dl_notcod.shape[0]
```

```python
# Write to CSV
df_noarchive_5yo_lt1000dl_notcod.to_csv("output.csv", index=False)
```