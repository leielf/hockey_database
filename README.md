# Hockey Database
Extracting data about hockey games and saving it into a database

## EliteProspects Player Database
Automatically scrapes player information (name, number, position, birthdate, profile URL) from the EliteProspects website and exports structured data for use in Notion.

**Features**:
1. Scrapes player data using BeautifulSoup.
2. Extracts:
   - Name
   - Jersey number
   - Position
   - Date of birth
   - EliteProspects profile link
3. Converts raw HTML into structured DataFrame.
4. Exports results to CSV/Excel for seamless integration into Notion.
**Used**: requests, BeautifulSoup, pandas, datetime

## Games Database
Merges data from Notion exports, RefAdmin Excel files, and SIHF game tables to generate a games dataset ready for import into Notion.

**Features**:
1. Team–City Mapping:
  Builds dictionaries linking team names and city names from Notion exports.
2. Referee Name Alignment:
  Matches RefAdmin referee names to the corresponding entries used in Notion.
3. Automated Game Creation:
  For each game:
     - Extracts home/away teams
     - Converts date formats
     - Checks league category
     - Generates SIHF game URLs automatically


<sup>(Note: Input files such as Excel/CSV exports from Notion and RefAdmin are not included in this repository for privacy)</sup>
