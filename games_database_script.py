import pandas as pd

def teams_dicts(noNL):
    city_names = noNL["Name"].values
    hometeams = noNL["Hometeam"].values
    away_teams = noNL["Away Team"].values
    cities_teams_dict = {}
    teams_cities_dict = {}
    home_cities = [name.split(" - ")[0] for name in city_names]
    away_cities = [name.split(" - ")[1] for name in city_names]
    add_to_dict_helper(home_cities, hometeams, cities_teams_dict, teams_cities_dict)
    add_to_dict_helper(away_cities, away_teams, cities_teams_dict, teams_cities_dict)
    return cities_teams_dict, teams_cities_dict

def add_to_dict_helper(cities, teams, cities_teams_dict, teams_cities_dict):
    for i in range(0, len(cities)):
        city_name = cities[i]
        if type(teams[i]) is float: continue
        team = teams[i]
        if team is not None and city_name not in cities_teams_dict.keys() and team not in teams_cities_dict.keys():
            cities_teams_dict[city_name] = team
            teams_cities_dict[team] = city_name


def create_ref_notion_dict(ref_df, ct_dict):
    refadmin_notion_dict = {}
    add_to_refadmin_dict_helper(ref_df["Equipe domicile"], ct_dict, refadmin_notion_dict)
    add_to_refadmin_dict_helper(ref_df["Equipe visiteur"], ct_dict, refadmin_notion_dict)
    return refadmin_notion_dict

def add_to_refadmin_dict_helper(column, ct_dict, refadmin_notion_dict):
    for city in ct_dict.keys():
        for refadmin_team in column:
            if city in refadmin_team:
                refadmin_notion_dict[refadmin_team] = ct_dict[city]
                break

def create_notion_crew_lst(notion_df):
    crew_arr = []
    for entry in notion_df["Crew"]:
        if type(entry) is float: continue
        for name in entry.split(","):
            if "[new person]" not in name: crew_arr.append(name)
    return crew_arr

def notion_reafdmin_ref_dict(crew_arr, ref_df):
    ref_dict = {}
    for col_name in ["H1", "H2", "L1", "L2"]:
        ref_dict_helper(ref_df[col_name], crew_arr, ref_dict)
    return ref_dict

def ref_dict_helper(col, crew_arr, dict):
    for ref in col:
        for ref_name in crew_arr:
            if ref in ref_name:
                dict[ref] = ref_name
                break

def create_name(away_team, tc_dict, home_team):
    if away_team in tc_dict.keys() and home_team in tc_dict.keys():
        return tc_dict[home_team] + " - " + tc_dict[away_team]
    else:
        return ""


def process_refadmin_date(refadmin_date):
    return refadmin_date.strftime('%d/%m/%Y')

def check_team(ref_name, rn_dict):
    if ref_name in rn_dict.keys():
        return rn_dict[ref_name]
    else:
        return ""

def add_team(ligue, teams, team):
    if ligue in ["SL", "NL"]:
        teams.append(team)
    else:
        teams.append("")

def add_url(sihf_df, date, home, away):
    for index, entry in sihf_df.iterrows():
        if date.replace("/", ".") == entry['Datum'] \
                and home in entry['Home'] and away in entry['Away']:
            return "https://www.sihf.ch/de/game-center/game/#/" + str(entry['Id'])
    return ""



def add_newdb(refadmin_df, tc_dict, rn_dict):
    sihf_table = pd.read_csv("shif_table.csv", sep=';')
    refadmin_df = refadmin_df.reset_index()
    names, home_teams, away_teams, dates, ligues, urls = [], [], [], [], [], []
    counter = 0
    for index, entry in refadmin_df.iterrows():
        away_team = check_team(entry["Equipe visiteur"], rn_dict)
        home_team = check_team(entry["Equipe domicile"], rn_dict)
        gamedate = process_refadmin_date(entry["Date/Heure"])
        name = create_name(away_team, tc_dict, home_team)
        if name == "":
            continue
        counter += 1
        ligue = entry["Catégorie ligue"]
        names.append(name)
        add_team(ligue, home_teams, home_team)
        add_team(ligue, away_teams, away_team)
        dates.append(gamedate)
        ligues.append(ligue)
        urls.append(add_url(sihf_table, gamedate, tc_dict[home_team], tc_dict[away_team]))
    status = ["Play"] * counter
    # "Name", "Status","Date","Ligue","Hometeam","Away Team","Crew"
    data = {'Name': names, 'Status': status,
              'Date': dates, 'Ligue': ligues,
              'Hometeam': home_teams, 'Away Team': away_teams, 'GameLink' : urls}
    new_df = pd.DataFrame(data)
    new_df.to_csv('output.csv', index=False)



#notion database
#creating dictionary for teams and there cities:
notion_fpath = "notion_games_more_games.csv"
notion_df = pd.read_csv(notion_fpath)
cities_teams_dict, teams_cities_dict = teams_dicts(notion_df)
crew_arr = create_notion_crew_lst(notion_df)


#refadmin database
file_path = "nico_database.xlsx"
refadmin_df = pd.read_excel(file_path)

ref_notion_dict = create_ref_notion_dict(refadmin_df, cities_teams_dict)

test_df = pd.read_excel("test.xlsx")
add_newdb(test_df, teams_cities_dict, ref_notion_dict)


# ValueError: No tables found
# pd_frames = pd.read_html(url)
# print(pd_frames[0])



