import csv
import os
import tqdm
import argparse
from dict_format import *


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'root_path',
        help='path where the files to merge are'
    )

    args = parser.parse_args()

    return args



def format_col(header_):

    col_format = []
    for col_name in header_:
        if col_name in FORMAT_COL.keys():
            col_format.append(FORMAT_COL.get(col_name))
        else:
            col_format.append(col_name)
    return col_format


def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = os.listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

def merge_files(args_):
    PATH = args_.root_path
    PATH_F = os.path.join(args_.root_path, "format_data")
    os.makedirs(PATH_F, exist_ok=True)
    files = find_csv_filenames(PATH)
    for file_id, file_dir in enumerate(files):
        rows = []
        file_dir = os.path.join(PATH, file_dir)
        with open(file_dir, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            header_f = format_col(header)
            for row in csvreader:
                rows.append(row)

        # Save new csv with format
        f = open(os.path.join(PATH_F, f"file_{file_id}.csv"), 'w')

        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(header_f)
        for row in rows:
            writer.writerow(row)
        # close the file
        f.close()

#
# # format bdd_spatial_DB.csv
# rows2 = []
# with open("./data/bdd_spatial_DB.csv", 'r') as file:
#     csvreader = csv.reader(file)
#     header2 = next(csvreader)
#     for row in csvreader:
#         rows2.append(row)
# print(header2)
# print(rows2[0:5])

if __name__ == "__main__":
    args = parse_args()
    merge_files(args)