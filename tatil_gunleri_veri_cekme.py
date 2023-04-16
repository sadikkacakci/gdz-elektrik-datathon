import requests
from bs4 import BeautifulSoup
import pandas as pd

def getDates(year,df):
    url = f"https://www.takvim.com/{year}_takvimi.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    liste = soup.find_all("p")
    all_values = liste[1].text
    all_values_list  = all_values.split("\n")
    all_dates_list = []
    for value in all_values_list:
        text_list = value.split("\t")
        date = text_list[0]
        date_list  = date.split(" ")

        if(len(date_list) == 2):
            try:
                date_list[0] = int(date_list[0])
            except:
                print(f"{date_list[0]} int'e çevrilmiyor.")
                continue
            all_dates_list.append(date_list)
    for list in all_dates_list:
        day = int(list[0])
        month = list[1]
        df = df.append({"day":day,"month":month,"year":year}, ignore_index = True)

    return df

def getDates2022(df): # 2022 özel durum
    year = "2022"
    url = f"https://www.takvim.com/{year}_takvimi.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    liste = soup.find_all("p")
    all_values = liste[1].text
    all_values_list  = all_values.split("\n")
    all_dates_list = []
    for value in all_values_list:
        if value == "1 Ocak\tYılbaşı":
            text_list = value.split("\t")
            date = text_list[0]
            date_list  = date.split(" ")
            date_list[0] = int(date_list[0])
            all_dates_list.append(date_list)
            continue
        date_list = value.split(" ")
        # print(date_list)
        if len(date_list) >= 2:
            try:
                date_list[0] = int(date_list[0])
                if(date_list[0]) > 31:
                    raise Exception(f"{date_list[0]} tarih için uygun değil.")
            except:
                print(f"{date_list[0]} int'e çevrilmiyor.")
                continue
            all_dates_list.append([date_list[0],date_list[1]])
    for list in all_dates_list:
        day = int(list[0])
        month = list[1]
        df = df.append({"day":day,"month":month,"year":year}, ignore_index = True)
    return df

years = ["2018","2019","2020","2021"]
df = pd.DataFrame(columns = ["day","month","year"])
for year in years:
   df = getDates(year,df)

df = getDates2022(df)

df.to_csv("tatil_gunleri_2018-2022.csv",index=False)