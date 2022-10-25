import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import datetime
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
from dict_indicators import *
from pygal_maps_fr.maps import Regions
from pathlib import Path
import os
import re


def find_xlsx_filenames(path_to_dir, suffix=".xlsx"):
    '''
    finding the excel files in specified path
    :param path_to_dir:
    :param suffix: xlsx excel files
    :return: list of xlsx files
    '''
    filenames = os.listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

def get_indicator_plots():
    '''
    create a excel file with bar plots of some columns from the DB-training
    '''

    print('#' * 80)
    print(' ' * 25+'Indicators for training programs'+' ' * 25)
    print('#' * 80)
    print('The database of the training programs must be in excel format, copy the absolut \n '
          'path of the excel file (e.g. C:\Copernicus_Project\Training_merged_DB_v6.xlsx)')
    PATH_E = input('and paste it here (.xlsx):')
    PATH_E = Path(PATH_E)
    PATH = PATH_E.parent
    PATH_I = os.path.join(PATH, "plot_indicators")
    os.makedirs(PATH_I, exist_ok=True)

    # Read csv file
    merged_df = pd.read_excel(PATH_E, 'Training_programs', index_col=None)

    # we select columns to plot
    col_info = ['Duration and terms', 'Way of training', 'Disciplines', 'Language',
                'Org. Country', 'Organisation', 'file', 'Diploma', 'Level Required']

    # create a list of stop words and adding custom stopwords
    stop_words = set(stopwords.words("english"))
    stop_words_f = set(stopwords.words("french"))

    # create a list of custom stopwords
    new_words =  CUSTOM_STOP
    stop_words = stop_words.union(new_words, stop_words_f)

    # remove unwanted columns keep selected headers
    dataset_ori = pd.DataFrame(merged_df, columns=col_info)
    dataset_fq = pd.DataFrame(merged_df, columns=col_info)

    # Data normalization
    print('#'*30+'Data normalization'+'#'*30)

    col_norm = ['Duration and terms', 'Way of training', 'Disciplines', 'Language']

    for col in tqdm(col_norm):
        # convert desc to string
        dataset_fq[col] = dataset_fq[col].astype(str)
        # convert to lowercase
        dataset_fq[col] = dataset_fq[col].str.lower()
        # cleaning stop words
        dataset_fq[col] = dataset_fq[col].apply(lambda x: ' '.join([item for item in x.split() if item not in stop_words]))

        dataset_fq[col] = dataset_fq[col].str.replace('[^\w\s]', '')

    dataset_fq = dataset_fq.replace(r'^\s*$', np.nan, regex=True)

    # Data consolidation
    print('#'*30+'Data Consolidation'+'#'*30)

    # - 0:Duration and terms
    data_0 = dataset_fq[col_info[0]].dropna()
    for row, id in tqdm(zip(data_0, data_0.index), total=len(data_0)):
        if 'year' in row:
            a = re.search('year', row)
            start = a.span()[0]
            data_0[id] = row[start-2: start+5]
        elif 'month' in row:
            a = re.search('month', row)
            start = a.span()[0]
            data_0[id] = row[start - 3: start + 6]
        elif 'semesters' in row:
            a = re.search('semesters', row)
            start = a.span()[0]
            data_0[id] = row[start - 2: start + 9]
        elif 'min' in row:
            data_0[id] = '<=1 day'

    dataset_fq[col_info[0]] = data_0

    dataset_fq[col_info[0]] = dataset_fq[col_info[0]].replace(DC_DURATION_TERMS)

    # - 1:Way of training
    data_1 = dataset_fq[col_info[1]].dropna()
    for row, id in tqdm(zip(data_1, data_1.index), total=len(data_1)):
        row = row.replace('sandwich', '')
        row = row.replace(' learning', '')
        row = row.replace('training', '')
        row = row.replace('initial', 'Int.')
        row = row.replace('education', 'Edu.')
        data_1[id] = row
    dataset_fq[col_info[1]] = data_1

    # - 2:Disciplines
    data_2 = dataset_fq[col_info[2]].dropna()
    for row, id in tqdm(zip(data_2, data_2.index),total=len(data_2)):
        row = row.replace('human social sciences', 'H&SS')
        row = row.replace('engineering', 'Eng.')
        row = row.replace('sciences', 'Sci.')
        row = row.replace('system', 'Sys.')
        row = row.replace('management production', 'PM')
        row = row.replace('programme', '')
        row = row.replace('applications', 'App.')
        data_2[id] = row
    dataset_fq[col_info[2]] = data_2

    # - 3:Language
    dataset_fq[col_info[3]] = dataset_fq[col_info[3]].replace(DC_LANGUAGE)

    # - 4:Org. Country
    data_4 = dataset_fq[col_info[4]].dropna()
    for row, id in tqdm(zip(data_4, data_4.index),total=len(data_4)):
        if 'Regions' in row:
            a = re.search('Regions', row)
            start = a.span()[1]
            data_4[id] = row[start+2:-1]

    dataset_fq[col_info[4]] = data_4

    dataset_fq[col_info[4]] = dataset_fq[col_info[4]].replace(DC_COUNTRY)

    # - 5:Organisation
    dataset_fq[col_info[5]] = dataset_fq[col_info[5]].replace(DC_ORGANISATION)

    # - 7:Diploma
    dataset_fq[col_info[7]] = dataset_fq[col_info[7]].replace(DC_DIPLOMA)

    # - 8:Level Required
    dataset_fq[col_info[8]] = dataset_fq[col_info[8]].replace(DC_LEVEL_REQUIRED)

    # create a writer for excel file
    writer = pd.ExcelWriter(PATH_I+'/indicators_plot.xlsx', engine='xlsxwriter')
    print('#'*30+'Getting indicators'+'#'*30)
    for col in tqdm(col_info):
        # dataset_fq[col] = dataset_fq[col].dropna()

        data2exp = dataset_fq[col].value_counts()
        data2exp.to_excel(writer, sheet_name=col)
        # figure
        plt.figure(figsize=(6, 5))
        data2exp[0:10, ].plot.bar()
        plt.ylabel('n')
        plt.title(col)
        plt.savefig(PATH_I+f'/{col}_freq.png', dpi=200, bbox_inches='tight')
        # new excel worksheet
        worksheet = writer.sheets[col]
        worksheet.insert_image('C2', PATH_I+f'/{col}_freq.png')


        if col=='Org. Country':
            reg_data = data2exp.to_dict()
            fr_chart = Regions(human_readable=True)
            today = datetime.today()
            datem = datetime(today.year, today.month, 1)

            fr_chart.title = 'Training programs by region'
            # fr_chart.add(f'In {datem}', aggregate_regions())
            fr_chart.add('In 2022', {'11': reg_data['Ile-de-France'], '82': reg_data['Auvergne-Rhône-Alpes'],
                                     '83': reg_data['Auvergne-Rhône-Alpes'], '73': reg_data['Occitanie'],
                                     '91': reg_data['Occitanie'], '93': reg_data['PACA'], '41': reg_data['Grand-Est'],
                                     '42': reg_data['Grand-Est'], '21': reg_data['Grand-Est'],
                                     '52': reg_data['Pays-de-la-Loire'], '54': reg_data['Nouvelle-Aquitaine'],
                                     '72': reg_data['Nouvelle-Aquitaine'], '74': reg_data['Nouvelle-Aquitaine'],
                                     '53': reg_data['Bretagne'], '22': reg_data['Hauts-de-France'],
                                     '31': reg_data['Hauts-de-France'], '23': reg_data['Normandie'],
                                     '25': reg_data['Normandie'], '26': reg_data['Bourgogne-Franche-Comté'],
                                     '43': reg_data['Bourgogne-Franche-Comté'], '24': reg_data['Centre-Val de Loire'],
                                     '03':reg_data['Guyane'], '02': reg_data['Martinique'], '04': reg_data['Réunion']})

            fr_chart.render_to_png(PATH_I+f'/{col}_chart.png')
            fr_chart.render_to_file(PATH_I + f'/{col}_chart.svg')
            worksheet.insert_image('K2', PATH_I+f'/{col}_chart.png')

        elif col == 'Organisation':
            ### Word Cloud
            dataset_fq[col] = dataset_fq[col].astype(str)
            #
            dataset_fq[col] = dataset_fq[col].apply(lambda x: ' '.join([item for item in x.split() if item not in stop_words]))
            #
            dataset_fq[col + 'new'] = dataset_fq[col].str.replace('[^\w\s]', '')

            comment_words = " ".join(cat for cat in dataset_fq[col + 'new'])

            wordcloud = WordCloud(width=800, height=800,
                                  background_color='white',
                                  stopwords=STOPWORDS,
                                  min_font_size=10).generate(comment_words)

            # plot the WordCloud image
            plt.figure(figsize=(8, 8), facecolor=None)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(PATH_I + f'/{col}_wordcloud.png', dpi=200, bbox_inches='tight')
            ###
            worksheet.insert_image('K2', PATH_I + f'/{col}_wordcloud.png')

        elif col == 'Disciplines':
            ### Word Cloud
            dataset_ori[col] = dataset_ori[col].astype(str)
            #
            dataset_ori[col] = dataset_ori[col].apply(lambda x: ' '.join([item for item in x.split() if item not in stop_words]))
            #
            dataset_ori[col + 'new'] = dataset_ori[col].str.replace('[^\w\s]', '')
            # Word cloud
            comment_words = " ".join(cat for cat in dataset_ori[col + 'new'])
            wordcloud = WordCloud(width=400, height=400,
                                  background_color='white',
                                  stopwords=STOPWORDS,
                                  min_font_size=5).generate(comment_words)

            # plot the WordCloud image
            plt.figure(figsize=(4, 4), facecolor=None)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(PATH_I + f'/{col}_wordcloud.png', dpi=200, bbox_inches='tight')
            ###
            worksheet.insert_image('K2', PATH_I + f'/{col}_wordcloud.png')


    # selected column headers we want to use
    new_headers = ['Title', 'Training Content']

    # remove unwanted columns keep selected headers
    dataset = pd.DataFrame(merged_df, columns=new_headers)

    for col in tqdm(new_headers):
        # convert desc to string
        dataset[col] = dataset[col].astype(str)
        # convert to lowercase
        dataset[col] = dataset[col].str.lower()
        # removing stop words
        dataset[col] = dataset[col].apply(lambda x: ' '.join([item for item in x.split() if item not in stop_words]))
        # removing special characters and empty spaces
        dataset[col+'new'] = dataset[col].str.lower().str.replace('[^\w\s]','')

        ### Word Cloud
        comment_words = " ".join(cat for cat in dataset[col+'new'])

        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              stopwords=STOPWORDS,
                              min_font_size=10).generate(comment_words)

        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.savefig(PATH_I + f'/{col}_wordcloud.png', dpi=200, bbox_inches='tight')

        # insert plots in excel file

        new_df = dataset[col+'new'].str.split(expand=True).stack().value_counts().reset_index()
        new_df.columns = ['Word', 'Frequency']
        new_df = new_df.set_index('Word')


        new_df.iloc[0:10, :].plot.bar()
        figure = plt.gcf()
        figure.set_size_inches(6, 5)

        plt.title(col)
        plt.savefig(PATH_I+f'/keyword_{col}.png', dpi=200, bbox_inches='tight')

        new_df.to_excel(writer, sheet_name='keywords_'+col)

        worksheet = writer.sheets['keywords_'+col]
        worksheet.insert_image('C2', PATH_I+f'/keyword_{col}.png')
        worksheet.insert_image('K2', PATH_I + f'/{col}_wordcloud.png')

    writer.save()

if __name__ == '__main__':
    get_indicator_plots()
    print('Process Finished')

