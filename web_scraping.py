from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import argparse
import tqdm
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--start_file',
        help = 'number of the initial file',
        type = int
    )
    parser.add_argument(
        '--final_file',
        help = 'number of the last file',
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
            print(f"#############{i}#############")

            #Title
            title = trainp[0].find("h3").string

            strong = trainp[0].find_all("strong")

            # Topics
            topics = trainp[0].find("Topics")
            topics = topics.parent.findNext('li').contents
            topics = ' '.join(topics)

            # Disciplines
            disciplines = trainp[0].find("Disciplines").parent.findNext('li').contents
            disciplines = ' '.join(disciplines)

            # Organization
            small = trainp[0].find_all("small")[0]
            org = small.string
            org = re.sub('[()]', '', org)
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

            p = trainp[0].find_all("p")
            obj_, pub_, deg_, adm_, pre_, dura_ = None, None, None, None, None, None
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
                            'Diploma': dipl, 'Level Required': title, 'URL': url_prog, 'Objectives': obj_, 'Public concerned': pub_,
                            'Degree Level (EU)': deg_, 'Admission requirements': adm_, 'Topics': topics, 'Disciplines': disciplines, 'Prerequisites': pre_, 'Duration and terms': dura_}, ignore_index=True)


    # save merged df to excel file
    df.to_excel("CNES_DB_probe.xlsx", sheet_name='CNES_Training_programs', index=False)
    #df.to_csv("CNES_DB_v0_v0.csv", sep=',', encoding='latin-1', index=False)


    #find specific tags
    # tag = doc.title
    # tags = doc.find_all("p")[0]
    #
    # print(tags)
    # print(tags.find_all("b"))

    #find specific text
    # prices = doc.find_all(text="$")
    # parent = prices[0].parent
    # print(parent)
    # strong = parent.find("strong")
    # print(strong.string)

    #links
    # for link in soup.find_all('a'):
    #     print(link.get('href'))
    # # http://example.com/elsie
    # # http://example.com/lacie
    # # http://example.com/tillie

if __name__ == "__main__":
    args =parse_args()
    run_scrapping(args)
