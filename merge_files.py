import csv
import os

import pandas as pd
import argparse
from dict_format import *
from tqdm import tqdm


def parse_args():
    '''
    use: python merge_files.py ./data/try_123
    the files must be in .csv format and the first row as the column names
    :return:
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'root_path',
        help='path where the files to merge are',
        default='/data/try_2'
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

def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = os.listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

def merge_files(args_):
    # the files must be csv format and the first row as the column names
    # format each file before merge
    PATH = args_.root_path
    PATH_F = os.path.join(PATH, "format_data")
    os.makedirs(PATH_F, exist_ok=True)
    files = find_csv_filenames(PATH)
    for file_id, file_dir in tqdm(enumerate(files)):
        rows = []
        file_name = file_dir.split('.')[0]
        file_dir = os.path.join(PATH, file_dir)
        with open(file_dir, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            header_f = format_col(header)
            for row in csvreader:
                rows.append(row)

        # Save new csv with format
        f_name = f"{file_name}_{file_id}.csv"
        f = open(os.path.join(PATH_F, f_name), 'w')

        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(header_f)
        for row in rows:
            writer.writerow(row)
        # close the file
        f.close()

    #merge
    all_files = find_csv_filenames(PATH_F)

    all_df = []
    for f in all_files:
        #TODO check if we can use the excel files directly instead of csv file, or add the option in the args
        df = pd.read_csv(os.path.join(PATH_F, f), sep=',', encoding='latin-1')
        df['file'] = f.split('/')[-1]
        all_df.append(df)

    merged_df = pd.concat(all_df, ignore_index=True, sort=True)

    # drop duplicates rows in the df
    merged_df = merged_df.drop_duplicates()
    print(merged_df.info())

    PATH_M = os.path.join(PATH, "merged_data")
    os.makedirs(PATH_M, exist_ok=True)

    # save merged df to excel file
    merged_df.to_excel(os.path.join(PATH_M, "Training_merged_DB_v3.xlsx"),
                       sheet_name='Training_programs', index=False, engine='xlsxwriter')
    #merged_df.to_csv(os.path.join(PATH_M, "Training_merged_DB_v3.csv"), sep=',', encoding='UTF-8', index=False)


if __name__ == "__main__":
    args = parse_args()
    merge_files(args)
