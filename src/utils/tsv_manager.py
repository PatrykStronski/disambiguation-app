import csv
import pandas as pd
from utils.logger import Logger
from config import CANDIDATES_FIELDS, CONLL_DELIMITER, POLEVAL_EXPORTED_FIELDS_UP, EXPORT_DIR

logger = Logger()

def write_conll(new_file, data, filename):
    dict_wrt = csv.DictWriter(new_file, POLEVAL_EXPORTED_FIELDS_UP, delimiter=CONLL_DELIMITER)
    dict_wrt.writeheader()
    for row in data:
        dict_wrt.writerow({key.upper(): row[key] for key in row.keys()})
    logger.successful("Output saved to " + EXPORT_DIR + filename + " file!")

def write_semeval_tsv(new_file, data, filename):
    dict_wrt = csv.DictWriter(new_file, ["from", "to", "wnid"], delimiter=CONLL_DELIMITER)
    for sentence in data:
        for row in sentence:
            dict_wrt.writerow({ "from": row["order_id"], "to": row["order_id"], "wnid": row["pwn_id"] })
    logger.successful("Output saved to " + EXPORT_DIR + filename + " file!")

def read_input_data(filename, format):
    """ parses data from files based on format and returns a DATAFRAME"""
    if not filename:
        logger.error("No Filename Chosen. Exiting!")
        return None
    read_file = open(EXPORT_DIR + filename, newline="")

    if format == "conll":
        parsed = csv.DictReader(read_file, delimiter=CONLL_DELIMITER)
        data = pd.DataFrame(columns=CANDIDATES_FIELDS)
        for row in parsed:
            data = data.append({key.lower(): row[key] for key in row.keys()}, ignore_index=True)
        if data.empty:
            logger.error("No data found for the provided file")
            return None
        return data

    logger.error("Format " + format + " not understood. Exiting")
    return None

def create_output_file(filename, data, format):
    """ Parses data back to file of format @format and saves it @data must be a list of dict """
    if not filename:
        logger.error("No Filename Chosen. Exiting!")
        return None
    new_file = open(EXPORT_DIR + filename, "w", newline="")

    if format == "conll":
        write_conll(new_file, data, filename)
        return None
    elif format == "semeval-tsv":
        write_semeval_tsv(new_file, data, filename)
        return None

    logger.error("Format " + format + " not understood. Exiting")
    return None
