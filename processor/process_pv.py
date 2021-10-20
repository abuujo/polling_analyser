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

from processor.measure_ci import measure_ci
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

