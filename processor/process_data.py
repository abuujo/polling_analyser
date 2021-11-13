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
    
# pass a party and build its own confidence interval
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


'''

This process takes our two party preferred vote that we have (somewhere)
and applys the Mackerras pendulum theory to find what seats could change hands given the polling.

This function - pass in the tpp preferences from both parties and use it to determine the swing 
in seats from the pendulumn file path (e.g. pre_election_pend_2019.csv)

In 2016, the lnp had a tpp vote of 50.36, and the alp had a tpp vote of 49.64
For the lnp and alp that represented a -3.13 and +3.13 % swing from their previous 2013 numbers
which would mean a "uniform" swing of 3.13% to the alp. 

The theory of the Mackerras pendulum states that the number of seats that are below that threshold will swap hands 
to the opposing major party (If they are the next major party)

Thus we can use this system in conjunction with our polling to add an extra column to the file we input
to say true or false if we believe with the latest numbers that one party will lose a seat and the other party 
(the second_party in the csv) gains it. 

'''
def mackerras_pendulum(lnp_tpp, alp_tpp, prev_party, prev_party_swing, pend_fp):

    pass


'''

The first part of my effort to build a weighted polling to see if I can make 
the polling available to us in Australia a little more reflective of where the actual votes
stand.

It's widely known that the polling done in 2019 was fairly innacurate, being more favorable to the
alp and less so to the lnp, based on the acutal performances of the two parties 
(note that to some extend, 2019 is an interesting election outside of the norm, considered
un-losable for the alp)

'''
def define_house_effect():
    pass

'''

After accounting for previous and present house effect's we can weight the polling based on
the overall tendancy for polling to be inaccurate. (note we mostly focus on tpp vote as
the election comes down to which seats change hands between the two major parties.)

'''

def prev_polling_err():
    pass