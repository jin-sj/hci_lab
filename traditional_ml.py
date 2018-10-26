""" Reads and parses fNIRS and MARKER data with traditional ML techniques

author: Seung Jung Jin
date: October 26, 2018
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn as sk

BASELINE_START = "baselinestart"
BASELINE_END = "baselineend"
EASY_START = "easystart"
EASY_END = "easyend"
HARD_START = "hardstart"
HARD_END = "hardend"

DEFAULT_FNIRS_PATH = os.path.join(os.getcwd(), "data/S902/2015-02-26_11-24-48-120", "fNIRSdata.txt")
DEFAULT_MARKER_PATH = os.path.join(os.getcwd(), "data/S902/2015-02-26_11-24-48-120", "markers.txt")

"""
Reads the fnirs and marker data

:param fnirs_path: Path to FNIRS data file
:param marker_path: Path to MARKER data file
:returns: Returns pandas dataframes for both files
"""
def read_data(fnirs_path=DEFAULT_FNIRS_PATH, marker_path=DEFAULT_MARKER_PATH):
    fnirs_df = pd.read_csv(fnirs_path, sep='\t', skiprows=range(4), index_col=False)
    marker_df = pd.read_csv(marker_path, sep='\t', skiprows=range(4), index_col=False)

    return fnirs_df, marker_df

"""
Discards data after "experimentfinished" and merges the two df

:param fnirs_df: fff
:param marker_df: fiejf
:returns: merged_df fij
"""
def clean_data(fnirs_df, marker_df):
    marker_df_end_row = marker_df.loc[marker_df["Stimulus_Label"] == "experimentfinished"]
    marker_df_end_time = marker_df_end_row["Matlab_now"].values[0]
    fnirs_df_end_row = fnirs_df.loc[fnirs_df["Matlab_now"] == marker_df_end_time]
    fnirs_df = fnirs_df[:fnirs_df_end_row.index[0]+1]
    marker_df = marker_df[:marker_df_end_row.index[0]+1]
    merged_df = pd.merge(fnirs_df, marker_df, on="Matlab_now", how="left")

    return merged_df


"""
Gets row blocks for each start and end of the task

:param merged_df:
:returns tuple of list of tuples of easy and hard tasks
"""
def get_start_end_row_blocks(merged_df):
    easy_start_rows = merged_df.index[merged_df.Stimulus_Label == EASY_START].tolist()
    easy_end_rows = merged_df.index[merged_df.Stimulus_Label == EASY_END].tolist()
    hard_start_rows = merged_df.index[merged_df.Stimulus_Label == HARD_START].tolist()
    hard_end_rows = merged_df.index[merged_df.Stimulus_Label == HARD_END].tolist()

    easy_rows = list(zip(easy_start_rows, easy_end_rows))
    hard_rows = list(zip(hard_start_rows, hard_end_rows))

    return easy_rows, hard_rows

"""
Plots the values

:param merged_df: DF to plot from
:param easy_rows: Blocks of easy task
:param hard_rows: Blocks of hard task
:returns: null
"""
def plot(merged_df, easy_rows, hard_rows, column_name):
    x = range(easy_rows[0][1] - easy_rows[0][0] + 1)
    y = merged_df.iloc[easy_rows[0][0]: easy_rows[0][1]+1]["A-DC1"].values.tolist()
    plt.plot(x, y)
    plt.show()

"""Main entrance"""
def main():
    print("Hello World!")

if __name__ == "__main__":
    main()

