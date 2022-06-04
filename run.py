import argparse
import os
import logging
import sys

from constants import FILE_DIRECTORY
from processor.process_data import establish_df 

'''
This system is ment to automate the process I go through to produce the 
confidence interval charts that I put on my site. This program will, in
the future,  be capable of automatically going through the process I
detail in order to "weight" polling agencies and types.
'''

logger = logging.getLogger(__name__)
logging.basicConfig(filename='process_output.log', encoding='utf-8', level=logging.DEBUG)

logging.info('File Root : %s', FILE_DIRECTORY)

def main(args):

    FILE_PATH = os.path.dirname(args.year+"/")

    FILE_DIRECTORY_YEAR = os.path.join(FILE_DIRECTORY, FILE_PATH)

    FILE_PATH_YEAR = os.path.join(FILE_DIRECTORY_YEAR, args.file)
    
    logging.info('File path set as : %s', FILE_PATH_YEAR)
    logging.info('File Directory set as : %s', args.type)

    my_list = [str(item) for item in args.list.split(',')]
    
    # Analyse Primary Vote
    if args.type == "PV":
        establish_df(FILE_PATH_YEAR, FILE_DIRECTORY_YEAR, logging, my_list, "primary_vote_", False)

    # Analyse Two Party Preferred 
    if args.type == "TPP":
        establish_df(FILE_PATH_YEAR, FILE_DIRECTORY_YEAR, logging, my_list, "two_party_pref_vote_", False)
        

    # Analyse Leadership Satisfaction
    if args.type == "LS":
        establish_df(FILE_PATH_YEAR, FILE_DIRECTORY_YEAR, logging, my_list, "leadership_satisfaction_vote_", args.person)

    # Analyse Preferred Prime Minister
    if args.type == "PPM":
        establish_df(FILE_PATH_YEAR, FILE_DIRECTORY_YEAR, logging, my_list, "preferred_prime_minister_vote_", False)
    
    print("Finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import csv')

    # Read in file location
    parser.add_argument('year'
    ,help="Election year - e.g. 2022, 2019 etc")

    parser.add_argument('file'
    ,help="File location to upload - e.g. pv.csv")

    # Read in file type 
    parser.add_argument('type'
    ,help="Data type : PV : Primary Vote \n TPP : Two Party Preferred \n LS : Leadership Satisfaction \n PPM : Preferred Prime Minister")

    # Grab columns - makes it easier to use one file
    parser.add_argument('-l', '--list', help='Input columns - e.g. -l p_lnp,p_alp,p_grn,p_onp,p_other', type=str, required=True)

    # Grab columns - makes it easier to use one file
    parser.add_argument('-p', '--person', help='Needed for Leadership = e.g. -p scomo', type=str, required=False)

    args = parser.parse_args()
    main(args)
