import argparse
import os
import logging
import sys

from constants import FILE_DIRECTORY

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

    FILE_PATH = os.path.join(FILE_DIRECTORY, args.file)
    
    logging.info('File path set as : %s', FILE_PATH)
    logging.info('File Directory set as : %s', args.type)
    
    # Analyse Primary Vote
    if args.type == "--PV":
        pass

    # Analyse Two Party Preferred 
    if args.type == "--TPP":
        pass

    # Analyse Leadership Satisfaction
    if args.type == "--LS":
        pass

    # Analyse Preferred Prime Minister
    if args.type == "--PPM":
        pass
    
    print("Finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import csv')

    # Read in file location
    parser.add_argument('file'
    ,help="File location to upload - e.g. pm.txt")

    # Read in file type 
    parser.add_argument('type'
    ,help="Data type : PV : Primary Vote \n TPP : Two Party Preferred \n LS : Leadership Satisfaction \n PPM : Preferred Prime Minister")

    args = parser.parse_args()
    main(args)
