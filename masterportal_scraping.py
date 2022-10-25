import requests, csv, re, time
from bs4 import BeautifulSoup as bs

main_url = "http://www.mastersportal.eu/countries/"
countries_res = requests.get(main_url)
countries_page = bs(countries_res.text,"lxml")

countries_headers = ["url","name","id"]
countries_file = open("countries.csv","a")
countries_csv = csv.DictWriter(countries_file, fieldnames = countries_headers)
countries_csv.writeheader()

universities_headers = ["url","name","id","country"]
universities_file = open("universities.csv","a")
universities_csv = csv.DictWriter(universities_file, fieldnames = universities_headers)
universities_csv.writeheader()

studies_headers = ["url","name","id","university","country"]
studies_file = open("studies.csv","a")
studies_csv = csv.DictWriter(studies_file, fieldnames = studies_headers)
studies_csv.writeheader()

for c in countries_page.select("#CountryOverview li a"):

    country_url = c['href'].encode('utf8')
    country_name = c['title'].encode('utf8')
    country_id = re.search("/\d+/",country_url).group()[1:-1]

    print("+", country_name, "("+country_id+")")

    countries_csv.writerow({
        "url": country_url.replace(",",""),
        "name": country_name.replace(",",""),
        "id": country_id.replace(",","")
    })

    universities_res = requests.get(country_url)
    universities_page = bs(universities_res.text,"lxml")

    for u in universities_page.select("#CountryStudies li a"):

        university_url = u['href'].encode('utf8')
        university_name = u['title'].encode('utf8')
        university_id = re.search("/\d+/",university_url).group()[1:-1]
        university_country = country_id

        print("++", university_name, "("+university_id+")")

        universities_csv.writerow({
            "url": university_url.replace(",",""),
            "name": university_name.replace(",",""),
            "id": university_id.replace(",",""),
            "country": university_country.replace(",","")
        })

        studies_res = requests.get(university_url)
        studies_page = bs(studies_res.text,"lxml")

        for s in studies_page.select("#StudyListing .StudyInfo a"):

            study_url = s['href'].encode('utf8')
            study_name = s['title'].encode('utf8')
            study_id = re.search("/\d+/",study_url).group()[1:-1]
            study_university = university_id
            study_country = country_id

            print("+++", study_name, "("+study_id+")")

            studies_csv.writerow({
                "url": study_url.replace(",",""),
                "name": study_name.replace(",",""),
                "id": study_id.replace(",",""),
                "university": university_id.replace(",",""),
                "country": country_id.replace(",","")
            })

            details_res = requests.get(study_url)
            with open("pages2/country-"+country_id+"_university-"+university_id+"_study-"+study_id+".html","w") as f:
                f.write(details_res.text.encode("utf-8"))

            time.sleep(2)

countries_file.close()
universities_file.close()
studies_file.close()
