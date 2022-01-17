from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import re
import os
import pandas as pd
import argparse
from tqdm import tqdm
from datetime import date


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--start_file',
        help = 'number of the initial file',
        required=True,
        type = int
    )
    parser.add_argument(
        '--final_file',
        help = 'number of the last file',
        required=True,
        type = int
    )

    args =parser.parse_args()

    return args

def run_scrapping(args_):

    df = pd.DataFrame()
    for i in tqdm(range(args_.start_file, args_.final_file)): #800-1678  last 2132
        url = f"https://www.formations-spatiales.fr/en/training-courses/{i}.htm"
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        # print(doc.prettify())
        trainp = doc.find_all("div", {"class": "margelateral"})
        if trainp[0].find_all("small"):

            #Title
            title = trainp[0].find("h3").string
            strong = trainp[0].find_all("strong")

            # Topics
            topics = None
            if trainp[0].find(string="Topics"):
                topics = trainp[0].find(string="Topics").findNext('ul').find_all('li')
                all_topics = []
                for tp in topics:
                    all_topics.append(tp.get_text())
                topics = ' '.join(all_topics)

            # Disciplines
            disciplines = None
            if trainp[0].find('h4', string="Disciplines"):
                disciplines = trainp[0].find('h4', string="Disciplines").findNext('ul').find_all('li')
                all_disciplines = []
                for dc in disciplines:
                    all_disciplines.append(dc.get_text())
                disciplines = ' '.join(all_disciplines)

            # Organization
            org = trainp[0].find("ul").find("li").find("a").get_text()

            # small = trainp[0].find_all("small")[0]
            # org = small.string
            # org = re.sub('[()]', '', org)

            # Way of training
            wot = strong[0].string

            # Languages
            lang = strong[1].string

            # Place
            place = None
            if trainp[0].find("li", string=re.compile("Place")):
                place_li = trainp[0].find("li", string=re.compile("Place"))
                place = place_li.string.split(":",1)[1]

            # Diploma
            dipl = None
            if trainp[0].find("li", string=re.compile("diploma")):
                dipl_li = trainp[0].find("li", string=re.compile("diploma"))
                dipl = dipl_li.string.split(":",1)[1]

            # Required level
            req_lvl = None
            if trainp[0].find("li", string=re.compile("level")):
                req_lvl_li = trainp[0].find("li", string=re.compile("level"))
                req_lvl = req_lvl_li.string.split(":",1)[1]

            # URL
            url_prog = None
            if trainp[0].find_all("a"):
                url_prog = trainp[0].find_all("a")[-1].get('href')
                # This is for checking if the page still exist code=200
                # try:
                #     if urlopen(url_prog).getcode() == 200:
                #         pass
                #     else:
                #         url_prog = None
                # except:
                #     url_prog = None

            p = trainp[0].find_all("p")
            obj_ = pub_ = deg_ = adm_ = pre_ = dura_ = None
            for pi in p:

                if pi.find("strong", string="Objectives"):
                    obj_ = pi.get_text().split(":",1)[1]
                elif pi.find("strong", string="Public concerned"):
                    pub_ = pi.get_text().split(":",1)[1]
                elif pi.find("strong", string="Degree Level (EU)"):
                    deg_ = pi.get_text().split(":",1)[1]
                elif pi.find("strong", string="Admission requirements"):
                    adm_ = pi.get_text().split(":",1)[1]
                elif pi.find("strong", string="Prerequisites"):
                    pre_ = pi.get_text().split(":",1)[1]
                elif pi.find("strong", string="Duration and terms"):
                    dura_ = pi.get_text().split(":",1)[1]

            df = df.append({'ID':i,'Title': title, 'Organisation': org, 'Way of training': wot, 'Language': lang, 'Place': place,
                            'Diploma': dipl, 'Level Required': req_lvl, 'URL': url_prog, 'Objectives': obj_, 'Public concerned': pub_,
                            'Degree Level (EU)': deg_, 'Admission requirements': adm_, 'Topics': topics, 'Disciplines': disciplines,
                            'Prerequisites': pre_, 'Duration and terms': dura_}, ignore_index=True)

    # save merged df to excel file
    today = date.today()
    PATH = os.path.join(os.getcwd(), "scrapping_data")
    os.makedirs(PATH, exist_ok=True)
    df.to_excel(os.path.join(PATH, f"CNES_DB_{today.day}-{today.month}-{today.year}.xlsx"), sheet_name='CNES_Training_programs', index=False)
    df.to_csv(os.path.join(PATH, f"CNES_DB_{today.day}-{today.month}-{today.year}.csv"), sep=',', encoding='UTF-8', index=False)


if __name__ == "__main__":
    args = parse_args()
    run_scrapping(args)
