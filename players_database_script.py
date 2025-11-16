# source /Users/leielf/Desktop/p_p/pythonProject/venv/bin/activate
import requests
import pandas as pd
from datetime import datetime
# ---------------------------------------------
# RAW HTML SCRAPING
# ---------------------------------------------

# def change_date_format(date):
#     return datetime.strptime(date, "%b %d, %Y").strftime("%m/%d/%Y")
#
# def get_date_of_birth(url):
#     response = requests.get(url)
#     lies = response.text.split("<li>")
#     for li in lies:
#         if "Date of Birth" in li:
#             li = li.strip("</li>").strip("</a>")
#             return li.split(">")[-1]
#     return ""
#
#
# def get_table(text):
#     tables = text.split("<table")
#     for tbl in tables:
#         if "GOALTENDERS" in tbl:
#             return tbl.split("/table>")[0]
#     return ""
#
# def get_name_url(td):
#     a = td.split("<a")[1].strip("</td>").strip("</div>").strip("</a>")
#     parts = a.split(">")
#     url = "https://www.eliteprospects.com" + parts[0].split("href=")[1][1:-1]
#     name = parts[1].split(" ")[0] + " " + parts[1].split(" ")[1].strip("<!--")
#     return url, name
#
# def process_tr(tr):
#     number = None
#     tds = tr.split("<td")
#     if "#" in tds[2]:
#         number = int(tds[2].split("#")[-1].strip("</td>"))
#     player_url, name = get_name_url(tds[4])
#     return number, name, player_url
#
#
# def process_players_by_position(tbody):
#     trs = tbody.split("<tr")
#     names, numbers, bddates, urls = [], [], [], []
#     trs.pop(0)
#     for tr in trs:
#         number, name, player_url = process_tr(tr)
#         bddate = change_date_format(get_date_of_birth(player_url))
#         names.append(name)
#         numbers.append(number)
#         bddates.append(bddate)
#         urls.append(player_url)
#     return names, numbers, bddates, urls
#
#
#
# team_table_url = "https://www.eliteprospects.com/team/4069/ehc-winterthur"
# content = response = requests.get(team_table_url)
# table = get_table(content.text)
# table_bodies = table.split("<tbody")
# POS = ["Goalie", "Defense", "Forward"]
# names, numbers, bddates, positions, urls = [], [], [], [], []
# for i in [2, 4, 6]:
#     tbnames, tbnumbers, tbbddates, tburls = process_players_by_position(table_bodies[i])
#     pos_i = int(i / 2 - 1)
#     for j in range(0, len(tbnames)):
#         names.append(tbnames[j])
#         numbers.append(tbnumbers[j])
#         bddates.append(tbbddates[j])
#         positions.append(POS[pos_i])
#         urls.append(tburls[j])
#
# data = {'Name': names, 'Group': 'Players', 'Number': numbers, 'Position': positions,
#               'Birthday': bddates, 'Eliteprospect': urls, 'Teams': '2025 SL Winterthur (https://www.notion.so/nd1/2025-SL-Winterthur-1da9f034536180a0b528f8d7862a1b57)'}
# players_df = pd.DataFrame(data)
# players_df.to_csv('automation_test_players.csv', index=False)


# --------------------------------------------------
# HTML SCRAPING USING BEAUTIFUL SOUP LIBRARY
# --------------------------------------------------

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_date_of_birth(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lies = soup.find_all('li')
    for li in lies:
        if "Date of Birth" in li.text:
            dob = li.text.split("h")[1].strip()
            print(dob)
            try:
                dob = datetime.strptime(dob, "%b %d, %Y").strftime("%m/%d/%Y")
            except:
                pass
            return dob
    return ""

def get_pos(pos, text):
    if "GOALTENDERS" in text:
        return 'Goalie'
    elif "DEFENSEMEN" in text:
        return 'Defense'
    elif "FORWARDS" in text:
        return 'Forward'
    return pos


team_url = "https://www.eliteprospects.com/team/4069/ehc-winterthur"
res = requests.get(team_url)
soup = BeautifulSoup(res.text, 'html.parser')

tables = soup.find_all('table')
data = []
tds = soup.find_all('td')
trs = tables[0].find_all('tr', class_="SortTable_tr__L9yVC")
pos = ""
for row in trs:
    cells = row.find_all('td')
    pos = get_pos(pos, row.text)
    if len(cells) >= 4:
        number = cells[1].text.strip().replace('#', '')
        link = cells[3].find('a')
        if link:
            text_parts = link.text.strip().split(" (")
            name = text_parts[0]
            player_url = "https://www.eliteprospects.com" + link['href']
            dob = get_date_of_birth(player_url)
            data.append([name, number, pos, dob, player_url])

df = pd.DataFrame(data, columns=["Name", "Number", "Position", "Birthday", "Eliteprospect"])
df.to_excel("players.xlsx", index=False)
print(df)
