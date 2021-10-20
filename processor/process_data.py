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

def establish_df(FILE_PATH, FILE_DIRECTORY_YEAR, logging, columns, name, leader_name):
    
    df = pd.read_csv(FILE_PATH, sep=',')

    # Unweighted File Path
    UNWEIGHTED_PATH = os.path.dirname("unweighted/")
    FILE_DIRECTOR_UNWEIGHTED = os.path.join(FILE_DIRECTORY_YEAR, UNWEIGHTED_PATH)

    logging.info("%s", FILE_DIRECTORY_YEAR)

    if not os.path.exists(FILE_DIRECTOR_UNWEIGHTED):
        os.makedirs(FILE_DIRECTOR_UNWEIGHTED)

    # These settings are assumed, but can be brought in through cms parser
    df['end_date'] =  pd.to_datetime(df['end_date'], format='%d/%m/%Y')
    df = df.sort_values(by=['end_date']) # Just in case

    # Unweighted Polling
    logging.info("Columns recorded: ")
    
    poll_data = df[["end_date"]]

    for item in columns:        
        analyse_party(item, df, logging, FILE_DIRECTOR_UNWEIGHTED, name)
        logging.info("%s", item)
        poll_data[item] = df[item]

    # Make Raw File for Scatter Plot
    poll_data = poll_data.melt(id_vars=['end_date'])
    poll_data['value'] = poll_data['value'].str.replace('%', '')
    poll_data = poll_data.dropna()

    file_str = name + "poll_data" + ".csv"
    if leader_name != False:
        file_str = leader_name + file_str # Unreasonably long name D:

    FILE_PATH_DF = os.path.join(FILE_DIRECTOR_UNWEIGHTED, file_str)
    logging.info("poll_data PATH set as : %s",FILE_PATH_DF)

    poll_data.to_csv(FILE_PATH_DF)
    
def analyse_party(party_name, df, logging, FILE_DIRECTOR_UNWEIGHTED, name):
    df_party = df[["end_date", party_name]]
    df_party.rename({party_name: 'value'}, axis=1, inplace=True)
    df_party['variable'] = party_name
    df_party = df_party.dropna()

    # Get CI
    df_party_ci = measure_ci(df_party)

    file_str = name + party_name + ".csv"
    FILE_PATH_DF = os.path.join(FILE_DIRECTOR_UNWEIGHTED, file_str)
    logging.info("DF PATH set as : %s",FILE_PATH_DF)
    df_party_ci.to_csv(FILE_PATH_DF)
    del df_party_ci

