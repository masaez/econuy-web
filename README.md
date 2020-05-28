<img src="https://i.imgur.com/o6cxmaP.jpg" width=400 style="margin-bottom:60px;">

  <a href="https://www.python.org/downloads/release/python-360/"><img src="https://img.shields.io/badge/python-=>3.6-blue.svg"></a>
  <a href="https://badge.fury.io/py/econuy"><img src="https://badge.fury.io/py/econuy.svg"></a>
  <a href="https://travis-ci.org/rxavier/econuy"><img src="https://travis-ci.org/rxavier/econuy.svg?branch=master"></a>
  <a href="https://codecov.io/gh/rxavier/econuy"><img src="https://codecov.io/gh/rxavier/econuy/branch/master/graph/badge.svg"></a>
  <a href="https://econuy.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/econuy/badge/?version=latest"></a>


This project simplifies gathering and processing of Uruguay economic statistics. Data is retrieved from (mostly) government sources and can be transformed in several ways (converting to dollars, calculating rolling averages, resampling to other frequencies, etc.).

If [this screenshot](https://i.imgur.com/Ku5OR0y.jpg) gives you anxiety, this package should be of interest:

# Installation

* PyPI:

```
pip install econuy
```

* Git:

```
git clone https://github.com/rxavier/econuy.git
cd econuy
python setup.py install
```

# Usage

**[Read the documentation](https://econuy.readthedocs.io/)**

## The `Session()` class

This is the recommended entry point for the package. It allows setting up the common behavior for downloads, and holds the current working dataset.

```
from econuy.session import Session

session = Session(data_dir="econuy-data", revise_rows="nodup", force_update=False, log=1, inplace=False)
```

The `Session()` object is initialized with the `data_dir`, `revise_rows`,  `force_update`, `dataset`, `log`, `logger` and `inplace` attributes.

* `location` controls where data will be saved and where it will be looked for when updating. It defaults to "econuy-data", and will create the directory if it doesn't exist.
* `revise_rows` controls the updating mechanism. It can be an integer, denoting how many rows from the data held on disk to replace with new data, or a string. In the latter case, `auto` indicates that the amount of rows to be replaced will be determined from the inferred data frequency, while `nodup` replaces existing data with new data for each time period found in both.
* `only_get` controls whether to get data from local sources or attempt to download it.
* `dataset` holds the current working dataset(s) and by default is initialized with an empty Pandas dataframe.
* `log` controls how logging works. `0`, don't log; `1`, log to console; `2`, log to console and file with default file; ``str``, log to console and file with filename=str.
* `logger` holds the current logger object from the logging module. Generally, the end user shouldn't set this manually.
* `inplace` controls whether transformation methods modify the current Session object inplace or whether they create a new instance with the same attributes (except `dataset`, of course).

### Session retrieval methods

#### `get()`

Downloads the basic datasets. These are basically as provided by official sources, except various Pandas transformations are performed to render nice looking dataframes with appropiate column names, time indexes and properly defined values.

Available options for the `dataset` argument are "cpi", "fiscal", "nxr", "naccounts", "labor", "rxr_custom", "rxr_official", "commodity_index", "reserves_chg" and "fx_ops". Most are self explanatory but all are explained in the documentation.

If you wanted CPI data:
```
df = session.get(dataset="cpi").dataset
```
Note that the previous code block accessed the `dataset` attribute in order to get a dataframe. Alternatively, one could also call the `final()` method after calling `get()`.

#### `get_frequent()`

Gives access to predefined data pipelines that output frequently used data. These are based on the datasets provided by `get()`, but are transformed to render data that you might find more immediately useful.

For example, the following downloads CPI data, calculates annual inflation (pct change from a year ago), monthly inflation, and seasonally adjusted and trend monthly inflation.
```
df = session.get_frequent(dataset="inflation")
```

### Session transformation methods

These class methods take a `Session()` object with a valid dataset and allow performing preset transformation pipelines. For example:
```
df = session.get(dataset="nxr").decompose(flavor="trend", outlier=True, trading=False)
```
will return a the Session object, with the dataset attribute holding the trend component of nominal exchange rate.

Available transformation methods are 
* `resample()` - resample data to a different frequency, taking into account whether data is of stock or flow type.
* `chg_diff()` - calculate percent changes or differences for same period last year, last period or at annual rate.
* `decompose()` - use X13-ARIMA to decompose series into trend and seasonally adjusted components.
* `convert()` - convert to US dollars, constant prices or percent of GDP.
* `base_index()` - set a period or window as 100, scale rest accordingly
* `rolling()` - calculate rolling windows, either average or sum.

## Retrieval functions

If you don't want to go the `Session()` way, you can simply get your data from the functions under `econuy.retrieval`, for example `econuy.retrieval.fiscal_accounts.get()`. While creating a Session object is recommended, this can be easier if you only plan on retrieving a single dataset.

## Dataframe/CSV headers

Metadata for each dataset is held in Pandas MultiIndexes with the following:

1) Indicator name
2) Topic or area
3) Frequency
4) Unit/currency
5) Current or inflation adjusted
6) Base index period(s) (if applicable)
7) Seasonal adjustment
8) Type (stock or flow)
9) Cumulative periods

## External binaries and libraries

### X13 ARIMA binary

If you want to use the `decompose()` method  you will need to supply the X13 binary (or place it somewhere reasonable and set `x13_binary="search"`). You can get it [from here](https://www.census.gov/srd/www/x13as/x13down_pc.html) for Windows or [from here](https://www.census.gov/srd/www/x13as/x13down_unix.html) for UNIX systems. For macOS you can compile it using the instructions found [here](https://github.com/christophsax/seasonal/wiki/Compiling-X-13ARIMA-SEATS-from-Source-for-OS-X) (choose the non-html version) or use my version (working under macOS Catalina) from [here](https://drive.google.com/open?id=1HxFoi57TWaBMV90NoOAbM8hWdZS9uoz_).

### unrar libraries

The [patool](https://github.com/wummel/patool) library is used in order to access fiscal data, which is provided by the MEF in `.rar` format. This library requires that you have the unrar binaries in your system, which you can get them from [here](https://www.rarlab.com/rar_add.htm).

----

# Problems and plans

## Problems

This project is heavily based on getting data from online sources that could change without notice, causing methods that download data to fail. While I try to stay on my toes and fix these quickly, it helps if you create an issue when you find one of these (or even submit a fix!).

## Plans

* ~~I now realize this project would greatly benefit from OOP and plan to implement it next.~~
* ~~Tests.~~
* CLI.
* Website.
* Automating data updates.
* Visualization.
