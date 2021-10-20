# Process the primary vote
# Create / access two folders - unweighted and weighted
# Unweighted - raw polling data - CI and Line
# Weighted - weighted polling data - CI and Line

# Imports
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.stats import expon as dist

from constants import FILE_DIRECTORY

UNWEIGHTED_PATH = os.path.dirname("unweighted/")
FILE_DIRECTOR_UNWEIGHTED = os.path.join(FILE_DIRECTORY, UNWEIGHTED_PATH)


if not os.path.exists(FILE_DIRECTOR_UNWEIGHTED):
    os.makedirs(FILE_DIRECTOR_UNWEIGHTED)

def establish_df(FILE_PATH,logging):
    df = pd.read_csv(FILE_PATH, sep=',')

    # These settings are assumed, but can be brought in through cms parser
    df['end_date'] =  pd.to_datetime(df['end_date'], format='%d/%m/%Y')
    df = df.sort_values(by=['end_date']) # Just in case

    # Unweighted Polling
    analyse_party("p_lnp", df, logging)
    analyse_party("p_alp", df, logging)
    analyse_party("p_grn", df, logging)
    analyse_party("p_other", df, logging)
    

def analyse_party(party_name, df, logging):
    df_party = df[["end_date", party_name]]
    df_party.rename({party_name: 'value'}, axis=1, inplace=True)
    df_party['variable'] = party_name

    # Get CI
    df_party_ci = measure_ci(df_party)

    file_str = party_name + ".csv"
    FILE_PATH_DF = os.path.join(FILE_DIRECTOR_UNWEIGHTED, file_str)
    logging.info("DF PATH set as : %s",FILE_PATH_DF)
    df_party_ci.to_csv(FILE_PATH_DF)
    del df_party_ci

def measure_ci(df):
    # Remove the % sign 
    df['value'] = df['value'].str.replace('%', '')
    df.value = pd.to_numeric(df.value)

    # Consider the 12 closest neighbouring polls to determine smoothed value
    # Min one to catch latest and earliest polls.
    df["smooth"] = df["value"].rolling(12,min_periods=1,win_type='hamming',center=True).mean()

    # Measure the noise value between the smoothed line and the actual value
    df["noise"] = df["value"] - df["smooth"]

    # Get higher values > 0 for asymetrical conf interval
    upper_noise = df[df["noise"] > 0]["noise"]
    upper_params = dist.fit(upper_noise)

    # Get lower values < 0
    lower_noise = (df[df["noise"] < 0]["noise"]).abs()
    lower_params = dist.fit(lower_noise)

    # 95 % conf interval - range of values we expect 95% of outcomes to be within
    upper_bound_value = dist.ppf(95/100, *upper_params)
    lower_bound_value = dist.ppf(95/100, *lower_params)

    # Add to the smoothed line
    df["ci_top"] = df["smooth"] + upper_bound_value
    df["ci_bot"] = df["smooth"] - lower_bound_value

    return df