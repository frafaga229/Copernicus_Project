import pandas as pd
import matplotlib.pyplot as plt
import argparse
from nltk.corpus import stopwords
import os


def parse_args():

    '''
    use: python indicators.py ./data/try_123

    :return:
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'path_file',
        help = 'path of the file to get plot indicators'
    )

    args = parser.parse_args()

    return args

def find_xlsx_filenames(path_to_dir, suffix=".xlsx"):
    filenames = os.listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

def get_indicator_plots(args_):
    '''
    create a excel file with bar plots of some columns from the DB-training

    '''
    PATH = args_.path_file
    PATH_M = os.path.join(PATH, "merged_data")
    PATH_I = os.path.join(PATH, "plot_indicators")
    os.makedirs(PATH_I, exist_ok=True)

    file_name = find_xlsx_filenames(PATH_M)[0]
    # Read csv file
    merged_df = pd.read_excel(PATH_M+f'/{file_name}', 'Training_programs', index_col=None)
    #merged_df = merged_df.to_csv('csvfile.csv', encoding='latin-1')
    #merged_df = pd.read_csv(PATH_M+f'/{file_name}', sep=',', encoding='latin-1')

    # we select columns to plot
    col_info = ['Duration and terms', 'Way of training', 'Disciplines', 'Language',
                'Org. Country', 'Organisation', 'file', 'Diploma', 'Level Required']

    # create a writer for excel file

    writer = pd.ExcelWriter(PATH_I+'/indicators_plot.xlsx', engine='xlsxwriter')
    for col in col_info:
        data2exp = merged_df[col].value_counts()
        data2exp.to_excel(writer, sheet_name=col)
        try:
            merged_df[col].value_counts()[0:10].plot.bar()
        except:
            pass
        figure = plt.gcf()
        figure.set_size_inches(6, 5)
        plt.ylabel('n')
        plt.title(col)
        plt.savefig(PATH_I+f'/{col}_freq.png', dpi=200, bbox_inches='tight')

        worksheet = writer.sheets[col]
        worksheet.insert_image('C2', f'{col}_freq.png')


    # selected column headers we want to use
    new_headers = ['Title', 'Training Content']
        # , 'Admission Requirements', 'Org. Country',
        #            'Prerequisites', 'Public concerned', 'Level Required']

    # remove unwanted columns keep selected headers
    dataset = pd.DataFrame(merged_df, columns=new_headers)

    # create a list of stop words and adding custom stopwords
    stop_words = set(stopwords.words("english"))
    stop_words_f = set(stopwords.words("french"))

    # create a list of custom stopwords
    new_words =  ['the', 'a ','us', 'sold', 'of', 'in', 'created', 'that', 'made', 'we\'ve', 'after', 'struggling','their','his','only','previously','leaving', 'et','c3s', 'otg',
                 'master', 'uls:', 'v4.0', 'efas', 'nan', 'rus', 'download', 'show', 'new', 'esa', 'use', 'free', 'service', 'access', 'learn', 'using', 'sar', 'acquired', 'analized',
                 'process', 'download', 'analyse', 'information', 'snap', 'visualize', 'employ', 'products', 'provides', 'efas', 'processing']

    stop_words = stop_words.union(new_words, stop_words_f)

    for col in new_headers:
        # convert desc to string
        dataset[col] = dataset[col].astype(str)
        # convert to lowercase
        dataset[col] = dataset[col].str.lower()
        #
        dataset[col] = dataset[col].apply(lambda x: ' '.join([item for item in x.split() if item not in stop_words]))
        #
        dataset[col+'new'] = dataset[col].str.lower().str.replace('[^\w\s]','')
        new_df = dataset[col+'new'].str.split(expand=True).stack().value_counts().reset_index()
        new_df.columns = ['Word', 'Frequency']
        new_df = new_df.set_index('Word')


        new_df.iloc[0:10, :].plot.bar()
        figure = plt.gcf()
        figure.set_size_inches(6, 5)

        plt.title(col)
        plt.savefig(f'keyword_{col}.png', dpi=200, bbox_inches='tight')

        new_df.to_excel(writer, sheet_name='keywords_'+col)

        worksheet = writer.sheets['keywords_'+col]
        worksheet.insert_image('C2', f'keyword_{col}.png')

    writer.save()

if __name__ == '__main__':
    args = parse_args()
    get_indicator_plots(args)

