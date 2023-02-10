import datetime
import requests
import bs4



def get_covid():
    url = "https://news.campaign.yahoo.com.tw/2019-nCoV/index.php"
    headers = {"User-Agent": "Mozilla/5.0", "Referer": url}
    re      = requests.get(url, headers = headers,verify=False,timeout=20)
    soup    = bs4.BeautifulSoup(re.content, 'html.parser')

    date  = soup.find_all(class_="secTaiwan")[0].text.split()
    print(date)
    TOTAL = date[3]
    TODAY = date[7]
    T_tol = date[8][2:]
    DEAD_ = date[-1][2:]
    came  = date[-5]
    D_TOD = date[-2]

    this_datatime = datetime.datetime.strptime(date[1][5:],"%Y年%m月%d日%H時%M分")
    data_date = this_datatime.strftime("%Y %#m/%#d")

    TODAY_DATE = datetime.datetime.now().strftime('%Y %#m/%#d')
    print(data_date,TODAY_DATE,data_date==TODAY_DATE)

    if (data_date != TODAY_DATE):
        TODAY_DATE = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y %#m/%#d')
        # print(data_date,TODAY_DATE,data_date==TODAY_DATE)
    
    
    message = f"""
=====================
{data_date}:
=====================
今日本土確診 : {TODAY} (包含校正回歸)
今日境外移入 : {came}
今日死亡人數 : {D_TOD}
=====================
本土累積確診 : {T_tol} 
全台累積確診 : {TOTAL}
全台累積死亡 : {DEAD_}   :skull_crossbones: :skull_crossbones: :skull_crossbones:
=====================
資料來源 : yahoo
"""
    return message


if __name__ == "__main__":
    print(get_covid())
