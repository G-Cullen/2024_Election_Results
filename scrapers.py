import csv
import datetime
import itertools
import requests
import pandas as pd
from bs4 import BeautifulSoup

def absentee_ballots():
    today = datetime.date.today()
    date_string = today.strftime("%Y%m%d")
    url = "https://elections.maryland.gov/press_room/2024_stats/PG24/Absentees%20Sent%20and%20Returned%20by%20County.xlsx"
    response = requests.get(url)
    with open(f"absentee/absentee_ballots_{date_string}.xlsx", 'wb') as output_file:
        output_file.write(response.content)

def process_ballots(date=datetime.date.today()):
    today = datetime.date.today()
    date_string = today.strftime("%Y%m%d")
    file_path = f"absentee/absentee_ballots_{date_string}.xlsx"
    data = pd.read_excel(file_path, skiprows=4)

    # Properly setting the header
    header_row = data.iloc[0]
    data = data[1:]

    # Set the header row as the dataframe header
    data.columns = header_row

    # Rename columns to fill NaN column names due to merged cells in Excel
    data.columns = ['Unknown' if pd.isna(name) else name for name in data.columns]

    # Drop columns labeled "Unknown"
    data = data.loc[:, ~data.columns.str.contains("Unknown")]

    # Drop rows that are completely empty
    data = data.dropna(how='all')

    # Save the column headers
    column_headers = data.columns.tolist()

    data = data[~data['CATEGORY'].isna()]

    # Drop rows where the first column value is 'CATEGORY' or the second column value is 'Total'
    #data = data[~((data['CATEGORY'] == 'CATEGORY') | (data.iloc[:, 1] == 'Total'))]

    # Save the cleaned data to CSV, ensuring no index and the correct headers are included
    filename_no_blanks_no_category = f'absentee/absentee_ballots_{date_string}.csv'
    data.to_csv(filename_no_blanks_no_category, index=False, header=column_headers)


if __name__ == "__main__":
    absentee_ballots()
    process_ballots()
